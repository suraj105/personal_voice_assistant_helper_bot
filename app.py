from flask import Flask, request , redirect

app = Flask(__name__)

@app.route('/')
def home():
    # 1. Capture the Lead's Name
    lead_name = request.args.get('id', 'Unknown Lead')

    # 2. Log the data to your terminal and file
    print(f"🔥 Success! {lead_name} clicked your link.")
    with open("leads.txt", "a") as f:
        f.write(f"Lead: {lead_name} clicked the link!\n")

    # 3. SEND traffic to destinated website
    return redirect("")


if __name__ == '__main__':
    app.run(port=5000)