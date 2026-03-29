from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────
#  FAKE ORDER DATABASE
#  Later: replace this with WooCommerce API calls
# ─────────────────────────────────────────────
ORDERS = {
    "EM1001": {
        "order_id": "EM1001",
        "customer_name": "Ravi Sharma",
        "product_name": "Apple iPhone 15 Pro (256GB, Black)",
        "order_status": "Out for Delivery",
        "tracking_id": "DTDC-998812345IN",
        "order_date": "2025-03-22",
        "estimated_delivery": "2025-03-29",
        "carrier": "DTDC Express",
        "status_code": "out_for_delivery"
    },
    "EM1002": {
        "order_id": "EM1002",
        "customer_name": "Priya Nair",
        "product_name": "Samsung 55\" QLED 4K Smart TV",
        "order_status": "Shipped",
        "tracking_id": "BLUEDART-77654321",
        "order_date": "2025-03-24",
        "estimated_delivery": "2025-03-31",
        "carrier": "Blue Dart",
        "status_code": "shipped"
    },
    "EM1003": {
        "order_id": "EM1003",
        "customer_name": "Arjun Mehta",
        "product_name": "Sony WH-1000XM5 Headphones",
        "order_status": "Processing",
        "tracking_id": "PENDING",
        "order_date": "2025-03-27",
        "estimated_delivery": "2025-04-02",
        "carrier": "Delhivery",
        "status_code": "processing"
    },
    "EM1004": {
        "order_id": "EM1004",
        "customer_name": "Meena Pillai",
        "product_name": "Dyson V15 Detect Vacuum Cleaner",
        "order_status": "Delivered",
        "tracking_id": "ECOM-EX-112233445",
        "order_date": "2025-03-18",
        "estimated_delivery": "2025-03-25",
        "carrier": "Ecom Express",
        "status_code": "delivered"
    },
    "EM1005": {
        "order_id": "EM1005",
        "customer_name": "Kiran Reddy",
        "product_name": "MacBook Air M3 (16GB RAM, 512GB SSD)",
        "order_status": "Order Confirmed",
        "tracking_id": "PENDING",
        "order_date": "2025-03-28",
        "estimated_delivery": "2025-04-03",
        "carrier": "Blue Dart",
        "status_code": "confirmed"
    },
}


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def home():
    """Serve the frontend tracking page."""
    return render_template("index.html")


@app.route("/track", methods=["POST"])
def track_order():
    """
    Accepts JSON: { "order_id": "EM1001" }
    Returns order details or an error message.

    WooCommerce upgrade note:
    Replace the ORDERS dict lookup below with a
    WooCommerce REST API call using the woocommerce
    Python library.
    """
    data = request.get_json()

    if not data or "order_id" not in data:
        return jsonify({
            "success": False,
            "error": "Please provide a valid Order ID."
        }), 400

    order_id = data["order_id"].strip().upper()
    order = ORDERS.get(order_id)

    if not order:
        return jsonify({
            "success": False,
            "error": f"No order found with ID '{order_id}'. Please check and try again."
        }), 404

    return jsonify({
        "success": True,
        "order": order
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({
        "status": "online",
        "service": "Everest Mart Order Tracker",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
