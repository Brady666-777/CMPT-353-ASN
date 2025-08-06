<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Copilot Instructions for Network Programming Assignment

This project demonstrates TCP and UDP client-server communication with RTT measurements.

## Project Context

- Socket programming in Python
- TCP vs UDP protocol comparison
- RTT (Round Trip Time) measurement
- Network performance analysis
- Port binding and protocol separation

## Coding Guidelines

- Use raw sockets (socket module) - no high-level frameworks
- Measure RTT excluding packet construction/parsing time
- Handle connection management properly for TCP
- Implement proper error handling and cleanup
- Use threading for concurrent connections when needed

## Key Concepts to Remember

- TCP is connection-oriented, UDP is connectionless
- TCP has connection establishment overhead
- UDP has lower latency but no reliability guarantees
- Different protocols can use the same port number
- RTT measurement should start just before send() and end just after recv()
