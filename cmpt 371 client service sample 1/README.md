# CMPT 371 Client-Server Communication Assignment

This project implements TCP and UDP client-server programs to demonstrate protocol differences and measure Round Trip Time (RTT) performance.

## Assignment Requirements

### Part A: Basic Client-Server Communication (4 marks)

- **TCP**: Client sends "hello TCP" to server on port 53333, server replies "back at you TCP"
- **UDP**: Client sends "Hello UDP" to server on port 53444, server replies "back at you UDP"
- Both measure and display RTT

### Part B: Protocol Comparison Analysis (2 marks)

Compare RTT performance between TCP and UDP protocols and explain the differences.

### Part C: Bulk Message Testing (2 marks)

Send 1000 consecutive messages with only one reply at the end. Compare TCP vs UDP performance.

### Part D: Same Port Protocol Testing (2 marks)

Run both TCP and UDP servers on port 53333, test if UDP server responds to TCP client.

## Project Structure

```
.
├── tcp_server.py          # TCP server (port 53333)
├── tcp_client.py          # TCP client with RTT measurement
├── udp_server.py          # UDP server (port 53444)
├── udp_client.py          # UDP client with RTT measurement
├── udp_server_53333.py    # UDP server for same-port testing
├── run_tests.py           # Comprehensive test suite
└── README.md              # This file
```

## Usage Instructions

### Method 1: Comprehensive Testing (Recommended)

Run the complete test suite that covers all assignment parts:

```bash
python run_tests.py
```

### Method 2: Manual Testing

#### TCP Testing:

1. Start TCP server:
   ```bash
   python tcp_server.py
   ```
2. In another terminal, run TCP client:
   ```bash
   python tcp_client.py
   ```

#### UDP Testing:

1. Start UDP server:
   ```bash
   python udp_server.py
   ```
2. In another terminal, run UDP client:
   ```bash
   python udp_client.py
   ```

#### Same Port Testing (Part D):

1. Start TCP server (uses port 53333):
   ```bash
   python tcp_server.py
   ```
2. Try to start UDP server on same port:
   ```bash
   python udp_server_53333.py
   ```
3. Run TCP client and observe behavior

## Expected Results

### Part A: Single Message RTT

- **UDP RTT**: Typically 0.5-2 ms (faster)
- **TCP RTT**: Typically 1-5 ms (slower due to connection overhead)

### Part B: Analysis

- **UDP** is faster for single messages because:
  - No connection establishment (3-way handshake)
  - No connection teardown
  - Less protocol overhead
- **TCP** is slower due to:
  - Connection setup/teardown overhead
  - Acknowledgment mechanisms
  - Flow control overhead

### Part C: Bulk Messages (1000 messages)

- **TCP** may perform better for bulk transfers because:
  - Connection is established once and reused
  - Better congestion control
  - Stream-oriented communication
- **UDP** maintains consistent performance but:
  - Each message is independent
  - No built-in reliability or ordering

### Part D: Same Port Testing

- **Result**: UDP server cannot respond to TCP client
- **Explanation**:
  - TCP and UDP are different transport protocols
  - Operating system routes packets based on protocol type
  - TCP connections require specific TCP handshake
  - UDP server listening on same port won't receive TCP packets

## Key Implementation Features

### RTT Measurement

- Uses `time.time()` for high-precision timing
- Starts timing just before `send()` call
- Stops timing just after `recv()` call
- Excludes packet construction and parsing time

### Error Handling

- Proper socket cleanup with try/finally blocks
- Connection timeout handling
- Server shutdown gracefully handles interrupts

### Threading Support

- TCP server handles multiple concurrent clients
- Each client connection runs in separate thread
- Daemon threads for automatic cleanup

## Technical Notes

### Socket Configuration

- TCP: `socket.AF_INET, socket.SOCK_STREAM`
- UDP: `socket.AF_INET, socket.SOCK_DGRAM`
- `SO_REUSEADDR` option prevents "Address already in use" errors

### Message Protocol

- Simple text-based messages
- UTF-8 encoding/decoding
- Fixed response patterns for automated testing

### Performance Considerations

- Local testing (localhost) minimizes network latency
- Results may vary on different systems
- Network conditions affect real-world performance

## Requirements

- Python 3.6+
- No external dependencies (uses built-in `socket` module)
- Windows/Linux/macOS compatible

## Assignment Deliverables

1. ✅ Source code files (tcp_server.py, tcp_client.py, udp_server.py, udp_client.py)
2. ✅ Test execution script (run_tests.py)
3. 📸 Screenshots of program execution (run `run_tests.py` and capture output)
4. 📝 Analysis explanations included in code comments and this README
