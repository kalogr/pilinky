# WORK IN PROGRESS

# 📟 Linky Teleinfo Reader

Python project to read and process teleinfo frames in **Standard mode** from a Linky smart meter using a Micro Téléinfo USB key connected to a Raspberry Pi.

---

## 🔧 Features

- Continuous reading of teleinfo frames from `/dev/ttyUSB0`
- Extraction and display of:
  - Instantaneous apparent power (`SINSTS`)
  - Total active energy (`EAST`)
  - Total active energy (`EASF02`)
- Data cleaning:
  - Removal of unnecessary leading zeros
  - Rejection of non-numeric or out-of-range values
  - Detection and exclusion of outlier values
- Rate-limited display to avoid flooding
- Logging with:
  - Daily log rotation
  - Retention of logs for 7 days

---

## 🗂️ Project Structure

```
teleinfo-test/
│
├── main.py               # Entry point of the program
├── reader.py             # Main class for reading and processing teleinfo frames
├── utils.py              # Utility functions for validating/filtering data
├── teleinfo.log          # Automatically generated log file
├── README.md             # This file
└── setup.sh              # Installation and auto-execution script
```

---

## 🚀 Running the Program

Make sure your USB key is recognized as `/dev/ttyUSB0`, then run:

```bash
python3 main.py
```

### 📦 Automated Installation and Execution

You can also automatically set up and start the program with:

```bash
./setup.sh
```

---

## ⚙️ Dependencies

- Python 3.7+
- Standard Python packages:
  - `serial`
  - `logging`
  - `statistics`
  - `collections`

To install `pyserial` if needed:

```bash
pip install pyserial
```

---

## 🛠️ Planned Improvements

- MQTT publishing of data
- Integration with a database (InfluxDB / SQLite)
- Visualization dashboard (Grafana / Home Assistant)

---

## 📝 Sample Processed Frame

```
SINSTS   00562
EAST     023294935
```

---

## 📒 Generated Logs

Each execution produces a `teleinfo.log` file with automatic daily rotation:

```
2025-05-12 13:42:03 [INFO] Instantaneous power (VA): 487
2025-05-12 13:42:10 [INFO] Total active energy (Wh): 23294935
```

---

## 👤 Author

Personal project by Kalo