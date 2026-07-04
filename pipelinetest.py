
import random
import time

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

MOLD_CLASSES = [
    "Aspergillus",
    "Cladosporium",
    "Penicillium",
    "Alternaria",
    "Stachybotrys",
    "Rhizopus",
    "Non-Mold"
]

# Typical enclosed, air-conditioned indoor room conditions
TEMP_RANGE_C = (20.0, 26.0)      # degrees Celsius
HUMIDITY_RANGE_RH = (40.0, 60.0) # percent relative humidity


# ---------------------------------------------------------------------------
# MOCK CAMERA + CLASSIFICATION STAGE
# ---------------------------------------------------------------------------

def simulate_camera_warmup(min_delay=1.5, max_delay=3.0):
    """
    Simulates the real-world delay of camera initialization
    and sample settling time on the substrate.
    """
    delay = random.uniform(min_delay, max_delay)
    print(f"[MOCK] Microscope warming up... ({delay:.1f}s)")
    time.sleep(delay)


def simulate_classification():
    """
    Returns a fake but plausible classification result, structured
    identically to what the real classify_mold.py would output.
    """
    predicted_label = random.choice(MOLD_CLASSES)
    mold_probability = round(random.uniform(0.55, 0.99), 3)
    return predicted_label, mold_probability


def run_mock_camera_cycle():
    """
    Simulates the full camera + inference cycle:
    camera on -> warm-up delay -> capture -> inference -> result.
    """
    print("[MOCK] Microscope camera: ON")
    simulate_camera_warmup()

    print("[MOCK] Capturing frame... (simulated)")
    time.sleep(0.5)

    print("[MOCK] Running inference... (simulated)")
    time.sleep(0.3)

    predicted_label, mold_probability = simulate_classification()

    print(f"[MOCK] Prediction: {predicted_label}")
    print(f"[MOCK] Confidence: {mold_probability:.3f}")

    return predicted_label, mold_probability


# ---------------------------------------------------------------------------
# MOCK BME280 SENSOR STAGE
# ---------------------------------------------------------------------------

def simulate_bme280(mode="auto", manual_temp=None, manual_humidity=None):
    """
    Simulates BME280 readings for an enclosed, air-conditioned room.

    mode:
        "auto"   -> generates a random realistic reading automatically
        "manual" -> prompts for input from the laptop terminal
    """
    if mode == "manual":
        if manual_temp is None:
            manual_temp = float(
                input(f"Enter simulated temperature (C) "
                      f"[{TEMP_RANGE_C[0]}-{TEMP_RANGE_C[1]} typical]: ")
            )
        if manual_humidity is None:
            manual_humidity = float(
                input(f"Enter simulated humidity (%RH) "
                      f"[{HUMIDITY_RANGE_RH[0]}-{HUMIDITY_RANGE_RH[1]} typical]: ")
            )
        temperature = manual_temp
        humidity = manual_humidity
    else:
        temperature = round(random.uniform(*TEMP_RANGE_C), 1)
        humidity = round(random.uniform(*HUMIDITY_RANGE_RH), 1)

    print(f"[MOCK BME280] Temperature: {temperature} C | Humidity: {humidity}% RH")
    return temperature, humidity


# ---------------------------------------------------------------------------
# ALLERGEN RISK SCORE (ARS) CALCULATION
# ---------------------------------------------------------------------------

def calculate_ars(mold_probability, temperature, humidity):
    """
    Placeholder weighted Allergen Risk Score formula.
    Replace the weights/logic below with your actual thesis ARS formula.

    Current placeholder logic:
        - Mold probability contributes the most (60%)
        - Humidity contributes next (30%) - higher humidity = higher risk
        - Temperature contributes least (10%) - normalized against 40C
    """
    ars = (mold_probability * 0.6) + (humidity / 100 * 0.3) + (temperature / 40 * 0.1)
    return round(ars, 3)


def interpret_ars(ars):
    """
    Simple placeholder risk-level bucketing for display purposes.
    Adjust thresholds to match your thesis's defined risk categories.
    """
    if ars < 0.4:
        return "Low"
    elif ars < 0.7:
        return "Moderate"
    else:
        return "High"


# ---------------------------------------------------------------------------
# FULL MOCK PIPELINE CYCLE
# ---------------------------------------------------------------------------

def run_full_mock_pipeline(sensor_mode="auto", cycle_number=None):
    """
    Runs one complete mock sampling cycle:
    camera/classification -> BME280 reading -> ARS calculation -> summary.
    """
    header = "=== Starting mock sampling cycle"
    if cycle_number is not None:
        header += f" #{cycle_number}"
    header += " ==="
    print(f"\n{header}")

    predicted_label, mold_probability = run_mock_camera_cycle()
    temperature, humidity = simulate_bme280(mode=sensor_mode)

    ars = calculate_ars(mold_probability, temperature, humidity)
    risk_level = interpret_ars(ars)

    print("\n--- Cycle Summary (Laptop Display) ---")
    print(f"Mold Type (mock):     {predicted_label}")
    print(f"Mold Confidence:      {mold_probability}")
    print(f"Temperature:          {temperature} C")
    print(f"Humidity:             {humidity}% RH")
    print(f"Allergen Risk Score:  {ars}")
    print(f"Risk Level:           {risk_level}")
    print("---------------------------------------")

    return {
        "label": predicted_label,
        "mold_probability": mold_probability,
        "temperature": temperature,
        "humidity": humidity,
        "ars": ars,
        "risk_level": risk_level
    }


# ---------------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    print("Mold Detection Device - MOCK Load Test Pipeline")
    print("This program simulates camera/model and BME280 readings.")
    print("No real hardware or trained model is used.\n")

    print("Select sensor input mode:")
    print("  1. Auto (randomly generated readings, no input needed)")
    print("  2. Manual (enter temperature/humidity yourself each cycle)")
    choice = input("Enter 1 or 2: ").strip()

    sensor_mode = "manual" if choice == "2" else "auto"

    try:
        num_cycles = int(input("How many sampling cycles to run? "))
    except ValueError:
        num_cycles = 1
        print("Invalid input, defaulting to 1 cycle.")

    results = []
    for i in range(1, num_cycles + 1):
        result = run_full_mock_pipeline(sensor_mode=sensor_mode, cycle_number=i)
        results.append(result)
        if i < num_cycles:
            time.sleep(1)  # simulate gap between sampling cycles

    print(f"\nCompleted {num_cycles} mock cycle(s).")


if __name__ == "__main__":
    main()
