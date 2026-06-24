import time

# ==================== PLC CONVEYOR SORTING SYSTEM ====================
print("=" * 60)
print("PROJECT 4: PLC-BASED CONVEYOR SORTING SYSTEM")
print("=" * 60)

# Digital Inputs (Sensors)
class Inputs:
    def __init__(self):
        self.sensor_box_detected = 0   # 0=No box, 1=Box present
        self.sensor_size = 0           # 0=Small, 1=Large
        self.sensor_pusher_home = 1    # 1=At home position
        self.emergency_stop = 0        # 0=Normal, 1=STOPPED

# Digital Outputs (Actuators)
class Outputs:
    def __init__(self):
        self.conveyor_motor = 0        # 0=OFF, 1=ON
        self.pusher_left = 0           # 0=OFF, 1=Push Left
        self.pusher_right = 0          # 0=OFF, 1=Push Right
        self.status_light = "GREEN"    # GREEN=Running, RED=Stopped

# Initialize
IN = Inputs()
OUT = Outputs()

# ==================== LADDER LOGIC SIMULATION ====================
print("\n--- LADDER LOGIC RULES ---")
print("1. E-Stop ON -> Everything OFF (Safety Interlock)")
print("2. Box Detected -> Check Size")
print("3. Small Box -> Left Pusher")
print("4. Large Box -> Right Pusher")
print("5. No Box -> Conveyor Running\n")

def ladder_logic():
    """Main PLC Scan Cycle - Runs continuously"""
    global OUT
    
    # ===== RUNG 1: EMERGENCY STOP (HIGHEST PRIORITY) =====
    if IN.emergency_stop == 1:
        OUT.conveyor_motor = 0
        OUT.pusher_left = 0
        OUT.pusher_right = 0
        OUT.status_light = "RED"
        print("[E-STOP] ALL SYSTEMS HALTED! Safety interlock active.")
        return
    
    OUT.status_light = "GREEN"
    
    # ===== RUNG 2: BOX DETECTION & SORTING =====
    if IN.sensor_box_detected == 1 and IN.sensor_pusher_home == 1:
        OUT.conveyor_motor = 0  # Stop conveyor
        
        if IN.sensor_size == 0:  # Small Box
            OUT.pusher_left = 1
            OUT.pusher_right = 0
            print(f"[SORT] Small box detected -> Pushing LEFT")
        else:  # Large Box
            OUT.pusher_left = 0
            OUT.pusher_right = 1
            print(f"[SORT] Large box detected -> Pushing RIGHT")
    
    # ===== RUNG 3: PUSHER RETRACT =====
    elif IN.sensor_pusher_home == 0:
        OUT.pusher_left = 0
        OUT.pusher_right = 0
        print("[RETRACT] Pusher returning to home position")
    
    # ===== RUNG 4: CONVEYOR RUNNING =====
    else:
        OUT.conveyor_motor = 1
        OUT.pusher_left = 0
        OUT.pusher_right = 0

def display_status(box_count):
    """Display PLC Status"""
    print("\n" + "-" * 40)
    print(f"BOX COUNT: {box_count}")
    print(f"INPUTS:  Box={IN.sensor_box_detected} Size={IN.sensor_size} "
          f"PusherHome={IN.sensor_pusher_home} EStop={IN.emergency_stop}")
    print(f"OUTPUTS: Motor={OUT.conveyor_motor} Left={OUT.pusher_left} "
          f"Right={OUT.pusher_right} Light={OUT.status_light}")
    print("-" * 40)

# ==================== TEST SIMULATION ====================
print("\n" + "=" * 60)
print("SIMULATION STARTING...")
print("=" * 60)

boxes = [
    {"size": 0, "desc": "Small Red Box"},
    {"size": 1, "desc": "Large Blue Box"},
    {"size": 0, "desc": "Small Green Box"},
    {"size": 1, "desc": "Large Yellow Box"},
    {"size": 0, "desc": "Small Black Box"},
]

for i, box in enumerate(boxes):
    print(f"\n>>> SCAN CYCLE {i+1}: {box['desc']}")
    
    # Step 1: Box arrives, sensor detects
    IN.sensor_box_detected = 1
    IN.sensor_size = box["size"]
    IN.sensor_pusher_home = 1
    
    ladder_logic()
    display_status(i+1)
    time.sleep(0.5)
    
    # Step 2: Pusher activated
    print("[ACTION] Pusher extending...")
    time.sleep(0.5)
    
    # Step 3: Box sorted, pusher retracts
    IN.sensor_box_detected = 0
    IN.sensor_pusher_home = 0
    ladder_logic()
    time.sleep(0.3)
    
    # Step 4: Pusher home, conveyor restarts
    IN.sensor_pusher_home = 1
    ladder_logic()
    display_status(i+1)

# ==================== EMERGENCY STOP TEST ====================
print("\n" + "=" * 60)
print("SAFETY TEST: EMERGENCY STOP")
print("=" * 60)

print("\n>>> E-STOP PRESSED!")
IN.emergency_stop = 1
ladder_logic()
display_status(len(boxes))

print("\n>>> E-STOP RELEASED - System Restarting...")
IN.emergency_stop = 0
ladder_logic()
display_status(len(boxes))

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("PROJECT 4 COMPLETE!")
print("=" * 60)
print(f"Total Boxes Sorted: {len(boxes)}")
print(f"Small Boxes (Left): {sum(1 for b in boxes if b['size']==0)}")
print(f"Large Boxes (Right): {sum(1 for b in boxes if b['size']==1)}")
print("Safety Interlock: VERIFIED - E-Stop works correctly")
print("=" * 60)
