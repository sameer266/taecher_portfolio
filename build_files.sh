# This script is used during Vercel deployment

echo "Building project..."

# Create python virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Build completed"