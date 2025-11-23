"""
Simple test to verify wellness_log.json functionality
"""
import json
import os
from datetime import datetime

WELLNESS_LOG_PATH = "wellness_log.json"


def test_create_sample_entry():
    """Create a sample wellness log entry for testing"""
    
    # Load existing log or create new
    if os.path.exists(WELLNESS_LOG_PATH):
        with open(WELLNESS_LOG_PATH, "r") as f:
            log_data = json.load(f)
    else:
        log_data = []
    
    # Create sample entry
    sample_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "mood": "energetic",
        "energy_level": "high",
        "objectives": "Complete Day 3 challenge, record demo video, post on LinkedIn",
        "stress_factors": "Excited about the challenge deadline!",
        "summary": "Mood: energetic, Energy: high. Goals: Complete Day 3 challenge, record demo video, post on LinkedIn"
    }
    
    log_data.append(sample_entry)
    
    # Save to file
    with open(WELLNESS_LOG_PATH, "w") as f:
        json.dump(log_data, f, indent=2)
    
    print(f"✅ Sample entry created successfully!")
    print(f"📝 Total entries in log: {len(log_data)}")
    print(f"\nLatest entry:")
    print(json.dumps(sample_entry, indent=2))


def test_read_entries():
    """Read and display all wellness log entries"""
    
    if not os.path.exists(WELLNESS_LOG_PATH):
        print("❌ No wellness_log.json file found. Run test_create_sample_entry() first.")
        return
    
    with open(WELLNESS_LOG_PATH, "r") as f:
        log_data = json.load(f)
    
    print(f"📊 Found {len(log_data)} check-in entries:\n")
    
    for i, entry in enumerate(log_data, 1):
        print(f"Entry {i} ({entry['date']} at {entry['time']}):")
        print(f"  • Mood: {entry['mood']}")
        print(f"  • Energy: {entry['energy_level']}")
        print(f"  • Objectives: {entry['objectives']}")
        if entry.get('stress_factors'):
            print(f"  • Stress: {entry['stress_factors']}")
        print()


if __name__ == "__main__":
    print("🧪 Testing Wellness Log Functionality\n")
    print("=" * 50)
    
    # Test 1: Create sample entry
    print("\nTest 1: Creating sample entry...")
    test_create_sample_entry()
    
    # Test 2: Read all entries
    print("\n" + "=" * 50)
    print("\nTest 2: Reading all entries...")
    test_read_entries()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print(f"\n💡 Tip: Check the {WELLNESS_LOG_PATH} file to see the persisted data.")
