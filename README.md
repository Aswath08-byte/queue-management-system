# queue-management-system
This is use to predict and ensure whether the customers are properly receiving the order through the tokens which are allotted to them and also this is not an full stack web or app ,this just an model and a prototype...!!!
# Varisai Canteen DM Notification Backend

This project includes a small Flask backend to send WhatsApp direct-message notifications when an order is ready.

## 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 2. Configure Twilio

Copy `.env.example` to `.env` and set your Twilio values:

```bash
copy .env.example .env
```

Then edit `.env` with your Twilio account SID, auth token, and WhatsApp number.

## 3. Run the backend

```bash
python server.py
```

The app will run on:

- http://localhost:5000

## 4. Use the app

Open the page in the browser, enter a mobile number, create the order, and then mark the item as ready. The backend will send a WhatsApp DM with the message:

> Your order is ready

## Notes

- This uses Twilio WhatsApp API for real direct-message delivery.
- If the Twilio config is missing, the app will fail safely and show an error in the response.
