#!/usr/bin/env python3
"""
Keep Alive Script for Render Deployment
This script helps keep your Render app awake by making periodic requests.
Run this locally to prevent your app from sleeping.
"""

import requests
import time
import sys

def keep_alive(url, interval=300):  # 5 minutes default
    """
    Keep the app alive by making periodic requests
    
    Args:
        url (str): Your app's URL (e.g., https://your-app.onrender.com)
        interval (int): Time between requests in seconds (default: 300 = 5 minutes)
    """
    print(f"🚀 Starting keep-alive for: {url}")
    print(f"⏰ Making requests every {interval} seconds")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            # Try the ping endpoint first (faster)
            response = requests.get(f"{url}/ping", timeout=10)
            if response.status_code == 200:
                print(f"✅ Ping successful at {time.strftime('%H:%M:%S')}")
            else:
                # Fallback to health check
                response = requests.get(f"{url}/health", timeout=10)
                if response.status_code == 200:
                    print(f"✅ Health check successful at {time.strftime('%H:%M:%S')}")
                else:
                    print(f"❌ Request failed with status {response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except KeyboardInterrupt:
            print("\n🛑 Keep-alive stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python keep_alive.py <your-app-url> [interval-seconds]")
        print("Example: python keep_alive.py https://your-app.onrender.com 300")
        sys.exit(1)
    
    app_url = sys.argv[1].rstrip('/')  # Remove trailing slash
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    
    keep_alive(app_url, interval) 