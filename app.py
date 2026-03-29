from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ─────────────────────────────────────────────
#  EMAIL CONFIG — loaded from environment variables
#  Set these in Render dashboard (never hardcode)
# ─────────────────────────────────────────────
EMAIL_USER = os.environ.get("EMAIL_USER")   # your Gmail address
EMAIL_PASS = os.environ.get("EMAIL_PASS")   # your Gmail App Password

# ─────────────────────────────────────────────
#  FAKE ORDER DATABASE
#  EM1001 uses your real Gmail for testing
#  Later: replace with WooCommerce API calls
# ─────────────────────────────────────────────
ORDERS = {
    "EM1001": {
        "order_id":           "EM1001",
        "customer_name":      "Ravi Sharma",
        "customer_email":     "kumarmoses432@gmail.com",
        "product_name":       "Apple iPhone 15 Pro (256GB, Black)",
        "order_status":       "Out for Delivery",
        "tracking_id":        "DTDC-998812345IN",
        "order_date":         "2025-03-22",
        "estimated_delivery": "2025-03-29",
        "carrier":            "DTDC Express",
        "status_code":        "out_for_delivery"
    },
    "EM1002": {
        "order_id":           "EM1002",
        "customer_name":      "Priya Nair",
        "customer_email":     "priyanair@gmail.com",
        "product_name":       "Samsung 55\" QLED 4K Smart TV",
        "order_status":       "Shipped",
        "tracking_id":        "BLUEDART-77654321",
        "order_date":         "2025-03-24",
        "estimated_delivery": "2025-03-31",
        "carrier":            "Blue Dart",
        "status_code":        "shipped"
    },
    "EM1003": {
        "order_id":           "EM1003",
        "customer_name":      "Arjun Mehta",
        "customer_email":     "arjunmehta@gmail.com",
        "product_name":       "Sony WH-1000XM5 Headphones",
        "order_status":       "Processing",
        "tracking_id":        "PENDING",
        "order_date":         "2025-03-27",
        "estimated_delivery": "2025-04-02",
        "carrier":            "Delhivery",
        "status_code":        "processing"
    },
    "EM1004": {
        "order_id":           "EM1004",
        "customer_name":      "Meena Pillai",
        "customer_email":     "meenapillai@gmail.com",
        "product_name":       "Dyson V15 Detect Vacuum Cleaner",
        "order_status":       "Delivered",
        "tracking_id":        "ECOM-EX-112233445",
        "order_date":         "2025-03-18",
        "estimated_delivery": "2025-03-25",
        "carrier":            "Ecom Express",
        "status_code":        "delivered"
    },
    "EM1005": {
        "order_id":           "EM1005",
        "customer_name":      "Kiran Reddy",
        "customer_email":     "kiranreddy@gmail.com",
        "product_name":       "MacBook Air M3 (16GB RAM, 512GB SSD)",
        "order_status":       "Order Confirmed",
        "tracking_id":        "PENDING",
        "order_date":         "2025-03-28",
        "estimated_delivery": "2025-04-03",
        "carrier":            "Blue Dart",
        "status_code":        "confirmed"
    },
}

# ─────────────────────────────────────────────
#  OTP STORE — in-memory
# ─────────────────────────────────────────────
OTP_STORE = {}


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(to_email, customer_name, order_id, otp):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Everest Mart OTP — Order {order_id}"
        msg["From"]    = EMAIL_USER
        msg["To"]      = to_email

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;
                    background:#0b0e14;color:#e8eaf0;border-radius:12px;
                    padding:32px;border:1px solid #1e2330;">
            <div style="text-align:center;margin-bottom:24px;">
                <span style="font-size:28px;">&#127956;</span>
                <h2 style="margin:8px 0;color:#ff6b3d;letter-spacing:-0.5px;">
                    Everest Mart
                </h2>
                <p style="color:#6b7280;font-size:13px;margin:0;">
                    Order Tracking Verification
                </p>
            </div>
            <p style="margin-bottom:8px;">Hi <strong>{customer_name}</strong>,</p>
            <p style="color:#9ca3af;font-size:14px;line-height:1.6;">
                You requested to track order
                <strong style="color:#e8eaf0;">{order_id}</strong>.
                Use the OTP below to verify your identity.
            </p>
            <div style="text-align:center;margin:28px 0;">
                <div style="background:#1a1f2e;border:1px solid #e8441a55;
                            border-radius:10px;padding:24px;display:inline-block;">
                    <p style="margin:0 0 8px;font-size:12px;color:#6b7280;
                               letter-spacing:1px;text-transform:uppercase;">
                        Your OTP Code
                    </p>
                    <p style="margin:0;font-size:42px;font-weight:700;
                               letter-spacing:12px;color:#ff6b3d;
                               font-family:monospace;">
                        {otp}
                    </p>
                </div>
            </div>
            <p style="color:#6b7280;font-size:13px;text-align:center;">
                This OTP expires in <strong style="color:#e8eaf0;">5 minutes</strong>.
                <br>Do not share this with anyone.
            </p>
            <hr style="border:none;border-top:1px solid #1e2330;margin:24px 0;">
            <p style="color:#4b5563;font-size:12px;text-align:center;margin:0;">
                &copy; 2025 Everest Mart &middot; If you did not request this, ignore this email.
            </p>
        </div>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        return True

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()

    if not data or "order_id" not in data or "email" not in data:
        return jsonify({"success": False, "error": "Please provide Order ID and Email."}), 400

    order_id = data["order_id"].strip().upper()
    email    = data["email"].strip().lower()

    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"success": False, "error": f"No order found with ID '{order_id}'."}), 404

    if order["customer_email"].lower() != email:
        return jsonify({"success": False, "error": "Email does not match our records for this order."}), 403

    otp     = generate_otp()
    expires = datetime.utcnow() + timedelta(minutes=5)

    OTP_STORE[order_id] = {
        "otp":      otp,
        "expires":  expires,
        "email":    email,
        "verified": False
    }

    sent = send_otp_email(email, order["customer_name"], order_id, otp)

    if not sent:
        return jsonify({"success": False, "error": "Failed to send OTP email. Please check server email config."}), 500

    return jsonify({"success": True, "message": f"OTP sent to {email[:3]}***@{email.split('@')[1]}"}), 200


@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()

    if not data or "order_id" not in data or "otp" not in data:
        return jsonify({"success": False, "error": "Please provide Order ID and OTP."}), 400

    order_id = data["order_id"].strip().upper()
    otp      = data["otp"].strip()

    session = OTP_STORE.get(order_id)
    if not session:
        return jsonify({"success": False, "error": "No OTP found for this order. Please request a new OTP."}), 404

    if datetime.utcnow() > session["expires"]:
        del OTP_STORE[order_id]
        return jsonify({"success": False, "error": "OTP has expired. Please request a new one."}), 410

    if otp != session["otp"]:
        return jsonify({"success": False, "error": "Incorrect OTP. Please check and try again."}), 401

    OTP_STORE[order_id]["verified"] = True

    return jsonify({"success": True, "message": "OTP verified successfully."}), 200


@app.route("/track", methods=["POST"])
def track_order():
    data = request.get_json()

    if not data or "order_id" not in data:
        return jsonify({"success": False, "error": "Please provide a valid Order ID."}), 400

    order_id = data["order_id"].strip().upper()

    session = OTP_STORE.get(order_id)
    if not session or not session.get("verified"):
        return jsonify({"success": False, "error": "Unauthorized. Please verify OTP first."}), 401

    del OTP_STORE[order_id]

    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"success": False, "error": f"No order found with ID '{order_id}'."}), 404

    return jsonify({"success": True, "order": order}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status":    "online",
        "service":   "Everest Mart Order Tracker",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
