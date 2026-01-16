from flask import jsonify, request
from application.model import *
from flask_jwt_extended import create_access_token, current_user, jwt_required
from datetime import datetime
from application.tasks import export_csv as export_csv_task, notify_user_booking
from .cache import cache


def routes(app):
    # ---------------------- SMARTPARK Home ----------------------
    @app.route("/api/base")
    def base():
        return jsonify(message="Welcome to SmartPark")
    

    # ---------------------- SMARTPARK Login ----------------------
    @app.route("/api/login", methods=['POST'])
    def login():
        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or user.password != password:
            return jsonify(message = 'Invalid credentials'), 401
        
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token, is_admin=user.is_admin, fullname=user.fullname)

    # ---------------------- SMARTPARK Register ----------------------
    @app.route("/api/register", methods=['POST'])
    def register():
        email = request.json.get('email')
        password = request.json.get('password')
        fullname = request.json.get('fullname')
        address = request.json.get('address')
        pincode = request.json.get('pincode')

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify(message="User already exists"), 409
        
        new_user = User(
            email = email,
            password = password,
            fullname = fullname,
            address = address,
            pin_code = pincode
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="User registered successfully!"), 201


    # ---------------------- Admin Dash ----------------------
    @app.route("/api/admin/dashboard")
    @jwt_required()
    def admin_dash():
        if not current_user.is_admin:
            return jsonify(message="Unauthorized"), 403
    
        total_lots = ParkingLot.query.count()
        total_spots = ParkingSpot.query.count()
        available_spots = ParkingSpot.query.filter_by(status='A').count()
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()

        return jsonify({
            "total_lots": total_lots,
            "total_spots": total_spots,
            "available_spots": available_spots,
            "occupied_spots": occupied_spots
        })

        
    # ---------------------- Parking Lots ----------------------
    @app.route("/api/parkinglots")
    @cache.cached(timeout=5)
    @jwt_required()
    def parkinglot():
        lots = ParkingLot.query.all()
        data = []
        for lot in lots:
            data.append({
                "id": lot.id,
                "name": lot.name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "total_spots": lot.total_spots,
                "spots": [
                    {"id": spot.id, "status": spot.status}
                    for spot in lot.spots
                ]
            })
        return jsonify(data)

    # ---------------------- Add Parking Lot ----------------------
    @app.route("/api/parkinglots", methods=["POST"])
    @jwt_required()
    def add_lot():
        if not current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        data = request.json

        name = data.get("name")
        price = data.get("price")
        address = data.get("address")
        pin_code = data.get("pin_code")
        total_spots = data.get("total_spots")

        if not name or not price or not address or not pin_code or not total_spots:
            return jsonify(message="All fields are required"), 400
        
        existing_name = ParkingLot.query.filter_by(name=name).first()
        existing_pin = ParkingLot.query.filter_by(pin_code=pin_code).first()

        if existing_name:
            return jsonify(message="Parking lot with this name already exists."), 409
        
        if existing_pin:
            return jsonify(message="Parking lot with this pin code already exists."), 409


        new_lot = ParkingLot(
            name=name,
            price=price,
            address=address,
            pin_code=pin_code,
            total_spots=total_spots
        )
        db.session.add(new_lot)
        db.session.commit()


        for _ in range(new_lot.total_spots):
            spot = ParkingSpot(lot_id=new_lot.id, status="A")
            db.session.add(spot)

        db.session.commit()

        return jsonify(message="Parking lot created", id=new_lot.id), 201
    

    # ---------------------- Delete Parking Lot ----------------------
    @app.route("/api/parkinglots/<int:lot_id>", methods=["DELETE"])
    @jwt_required()
    def delete_lot(lot_id):
        if not current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify(message="Parking lot not found"), 404

    
        occupied_spot = ParkingSpot.query.filter_by(lot_id=lot.id, status="O").first()
        if occupied_spot:
            return jsonify(message="Cannot delete! Some spots are occupied."), 400

    
        ParkingSpot.query.filter_by(lot_id=lot.id).delete()

    
        db.session.delete(lot)
        db.session.commit()

        return jsonify(message="Parking lot deleted successfully"), 200
    


    # ---------------------- Edit Parking Lot ----------------------
    @app.route("/api/parkinglots/<int:lot_id>", methods=["PUT"])
    @jwt_required()
    def edit_lot(lot_id):
        if not current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify(message="Parking lot not found"), 404


        occupied_spot = ParkingSpot.query.filter_by(lot_id=lot.id, status="O").first()
        if occupied_spot:
            return jsonify(message="Cannot edit. Some spots are occupied."), 400

        data = request.json

        lot.name = data.get("name", lot.name)
        lot.price = data.get("price", lot.price)
        lot.address = data.get("address", lot.address)
        lot.pin_code = data.get("pin_code", lot.pin_code)

        new_total = data.get("total_spots", lot.total_spots)

        if new_total != lot.total_spots:
            if new_total > lot.total_spots:
                for _ in range(new_total - lot.total_spots):
                    new_spot = ParkingSpot(lot_id=lot.id, status="A")
                    db.session.add(new_spot)

            elif new_total < lot.total_spots:
                removable_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status="A")\
                                                .order_by(ParkingSpot.id.desc())\
                                                .limit(lot.total_spots - new_total)\
                                                .all()
                if len(removable_spots) < (lot.total_spots - new_total):
                    return jsonify(message="Not enough available spots to reduce."), 400
                for spot in removable_spots:
                    db.session.delete(spot)

            lot.total_spots = new_total

        db.session.commit()
        return jsonify(message="Parking lot updated successfully"), 200
    
    # ---------------------- Admin View Spots ----------------------
    @app.route("/api/parkinglots/<int:lot_id>/spots")
    @jwt_required()
    def view_spot(lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify(message="Parking lot not found"), 404

        spots = [
            {"id": spot.id, "status": spot.status}
            for spot in lot.spots
        ]
        return jsonify({
            "lot_id": lot.id,
            "lot_name": lot.name,
            "spots": spots
        }), 200
    
    # ---------------------- Admin View Users ----------------------
    @app.route("/api/users")
    @jwt_required()
    def view_users():
        if not current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        users = User.query.filter_by(is_admin=False).all()

        data = []
        for user in users:
            data.append({
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email,
                "address": user.address,
                "pin_code": user.pin_code
            })
        return jsonify(data), 200
    
    # ---------------------- Admin View User Details ----------------------
    @app.route("/api/users/<int:user_id>")
    @jwt_required()
    def user_details(user_id):
        if not current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify(message="User not found"), 404

        reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()
        
        booking_history = []
        for res in reservations:
            lot = res.spot.lot if res.spot else None
            booking_history.append({
                "reservation_id": res.id,
                "lot_name": lot.name if lot else "N/A",
                "parking_timestamp": res.parking_timestamp.strftime("%Y-%m-%d %H:%M") if res.parking_timestamp else None,
                "leaving_timestamp": res.leaving_timestamp.strftime("%Y-%m-%d %H:%M") if res.leaving_timestamp else None,
                "parking_cost": res.parking_cost or 0,
                "vehicle_number": res.vehicle_number
            })

        data = {
            "fullname": user.fullname,
            "email": user.email,
            "address": user.address,
            "pin_code": user.pin_code,
            "booking_history": booking_history
        }

        return jsonify(data), 200


    # ---------------------- User Dash ----------------------
    @app.route("/api/user/dashboard")
    @jwt_required()
    def user_dash():
        if current_user.is_admin:
            return jsonify(message="Unauthorized"), 403
        return jsonify(message="Welcome to User Dashboard!")
    

    # ---------------------- User Book Spot ----------------------
    @app.route("/api/book", methods=["POST"])
    @jwt_required()
    def book_spot():
        if current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        data = request.json
        lot_id = data.get("lot_id")
        vehicle_number = data.get("vehicle_number", "").upper()

        if not vehicle_number:
            return jsonify(message="Vehicle Number are required"), 400


        existing = Reservation.query.filter_by(
            vehicle_number=vehicle_number,
            leaving_timestamp=None
        ).first()
        if existing:
            return jsonify(message="This vehicle is already parked!"), 400


        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first()
        if not spot:
            return jsonify(message="No available spots in this lot"), 400


        spot.status = "O"
        lot = ParkingLot.query.get(lot_id)

        reservation = Reservation(
            user_id=current_user.id,
            spot_id=spot.id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.now(),
            parking_cost=lot.price
        )

        db.session.add(reservation)
        db.session.commit()
        notify_user_booking.delay(current_user.fullname, lot.name)

        return jsonify(
            message="Booking Successful!",
            reservation_id=reservation.id,
            lot_id=lot.id,
            spot_id=spot.id,
            price=lot.price
        ), 201
    

    # ---------------------- User Reservations ----------------------
    @app.route("/api/user/reservations")
    @jwt_required()
    def reservations():
        if current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.parking_timestamp.desc()).all()

        data = []
        for res in reservations:
            duration = None
            if res.leaving_timestamp:
                duration = str(res.leaving_timestamp - res.parking_timestamp)

            data.append({
                "id": res.id,
                "lot_id": res.spot.lot_id if res.spot else None,
                "lot_name": res.spot.lot.name if res.spot and res.spot.lot else None,
                "spot_id": res.spot_id,
                "parking_timestamp": res.parking_timestamp.strftime("%d-%m-%Y %H:%M"),
                "leaving_timestamp": res.leaving_timestamp.strftime("%d-%m-%Y %H:%M") if res.leaving_timestamp else None,
                "vehicle_number": res.vehicle_number,
                "cost": res.parking_cost
            })
        return jsonify(data), 200
    
    # ---------------------- Release Spot ----------------------
    @app.route("/api/release/<int:reservation_id>", methods=["PUT"])
    @jwt_required()
    def release_spot(reservation_id):
        if current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        res = Reservation.query.get(reservation_id)
        if not res or res.user_id != current_user.id:
            return jsonify(message="Reservation not found"), 404

        if res.leaving_timestamp:
            return jsonify(message="Already released"), 400

        res.leaving_timestamp = datetime.now()

        duration_seconds = (res.leaving_timestamp - res.parking_timestamp).total_seconds()
        hours = max(1, int((duration_seconds + 3599) // 3600))

        lot = res.spot.lot
        res.parking_cost = hours * lot.price

        res.spot.status = "A"

        db.session.commit()

        return jsonify({
            "reservation_id": res.id,
            "lot_name": lot.name,
            "lot_id": lot.id,
            "duration_hours": hours,
            "total_price": res.parking_cost,
            "parking_time": res.parking_timestamp.strftime("%d-%m-%Y %H:%M"),
            "leaving_time": res.leaving_timestamp.strftime("%d-%m-%Y %H:%M"),
            "vehicle_number": res.vehicle_number
        }), 200
    
    # ---------------------- User Summary ----------------------
    @app.route("/api/user/dashboard/summary")
    @jwt_required()
    def user_summary():
        if current_user.is_admin:
            return jsonify(message="Unauthorized"), 403

        total_bookings = Reservation.query.filter_by(user_id=current_user.id).count()
        active_bookings = Reservation.query.filter_by(user_id=current_user.id, leaving_timestamp=None).count()
        completed_bookings = Reservation.query.filter(
            Reservation.user_id == current_user.id,
            Reservation.leaving_timestamp.isnot(None)
        ).count()

        total_spent = db.session.query(db.func.sum(Reservation.parking_cost)).filter_by(user_id=current_user.id).scalar() or 0.0

        return jsonify({
            "total_bookings": total_bookings,
            "active_bookings": active_bookings,
            "completed_bookings": completed_bookings,
            "total_spent": round(total_spent, 2)
        })


    
    # ---------------------- Export User CSV ----------------------
    @app.route("/api/export_csv", methods=["POST"])
    @jwt_required()
    def export_user_csv():
        if current_user.is_admin:
            return jsonify(message="Admins cannot export user data."), 403

        try:
            task = export_csv_task.delay(current_user.id)
            return jsonify(message="CSV export downloaded", task_id=task.id), 202
        except Exception as e:
            return jsonify(message=f"Export failed: {str(e)}"), 500