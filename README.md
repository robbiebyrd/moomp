# MOOMP

**Multi-User Dungeon, Object Oriented with Mongo and Python**

A modern MOO-like (MUD Object Oriented) server implementation written in Python, using MongoDB for persistent storage, MQTT for real-time messaging, and Lua for in-game object scripting.

---

## Table of Contents

- [Purpose](#purpose)
- [Features](#features)
- [Technologies Used](#technologies-used)
  - [Programming Languages](#programming-languages)
  - [Frameworks and Libraries](#frameworks-and-libraries)
  - [Applications and Services](#applications-and-services)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation Instructions](#installation-instructions)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Entrypoints](#entrypoints)
  - [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)
  - [Directory Structure](#directory-structure)
  - [Entrypoints](#entrypoints-1)
  - [Key Components](#key-components)
- [Included Packages and Dependencies](#included-packages-and-dependencies)

---

## Purpose

MOOMP is a text-based multi-user virtual environment server that enables players to interact in real-time within a shared virtual world. It provides a platform for building and exploring interactive text-based worlds, reminiscent of classic MUD (Multi-User Dungeon) systems but with modern architecture and technologies.

The server supports:
- Real-time player interaction and communication
- Object-oriented world building with dynamic properties
- Scriptable game objects using Lua
- Role-based access control for world management
- Persistent world state using MongoDB
- Real-time event notifications via MQTT

---

## Features

- **Multi-User Environment**: Support for concurrent players connecting via Telnet
- **Object-Oriented Design**: Characters, Objects, Rooms, and Portals as first-class entities
- **Real-Time Messaging**: MQTT-based event system for instant updates
- **Scriptable Objects**: Lua scripting support for dynamic game logic
- **Role-Based Access**: Configurable roles (Programmer, Admin, Manager) with different permissions
- **Rich Text Interface**: ANSI color support with customizable themes
- **World Building Tools**: In-game commands for creating and modifying the world
- **Inventory System**: Object management and carrying mechanics
- **Navigation**: Portal-based room navigation with aliases and descriptions
- **Persistent Storage**: MongoDB backend for data persistence
- **User Authentication**: Secure account management with password policies
- **Waypoint System**: Bookmark and fast-travel to favorite locations
- **Speech System**: Multiple communication methods (say, whisper, etc.)

---

## Technologies Used

### Programming Languages

- **Python 3.12**: Primary application language
- **Lua**: In-game scripting engine via Lupa
- **JSON**: Configuration and data serialization

### Frameworks and Libraries

- **MongoEngine**: MongoDB ODM (Object-Document Mapper)
- **Pydantic**: Data validation and settings management
- **Paho MQTT**: MQTT client for message broker communication
- **Telnetlib3**: Telnet server implementation
- **Bcrypt**: Secure password hashing
- **Cheetah3**: Template engine for dynamic text generation
- **LangChain**: AI/LLM integration framework
- **Email-Validator**: Email address validation
- **Pluralizer**: Text pluralization utilities
- **ANSI-Escapes**: Terminal control sequences

### Applications and Services

- **MongoDB**: NoSQL database for persistent storage
- **Eclipse Mosquitto**: MQTT message broker
- **Docker**: Containerization and orchestration
- **Poetry**: Python dependency management

---

## Getting Started

### Prerequisites

Before running MOOMP locally, ensure you have the following installed:

- **Python 3.12** or higher
- **Poetry** (Python dependency manager)
- **Docker** and **Docker Compose**
- **Git** (for cloning the repository)

### Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/robbiebyrd/moomp.git
   cd moomp
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure your settings if needed. Default values are provided for local development.

3. **Start required services** (MongoDB and MQTT):
   ```bash
   docker-compose up -d
   ```

4. **Install Python dependencies**:
   ```bash
   poetry install
   ```

5. **Seed the database** (first-time setup):
   ```bash
   poetry run python main.py seed --seed_file ./seeds/1.json
   ```

---

## Usage

### Running Locally

Start the Telnet server:

```bash
poetry run python main.py telnet Hereville
```

The server will start on port `7890` (default). Connect using any Telnet client:

```bash
telnet localhost 7890
```

### Entrypoints

MOOMP provides multiple entrypoints for different services:

- **Telnet Server**: `python main.py telnet <instance_name>`
  - Starts the main Telnet server for player connections
  
- **MQTT Consumer**: `python main.py mqtt <instance_name>`
  - Starts the MQTT message consumer for real-time updates
  
- **Database Seeding**: `python main.py seed --seed_file <path>`
  - Initializes or updates the database with seed data
  
- **LLM Integration**: `python main.py llm <instance_name>`
  - Starts the AI/LLM integration server (experimental)

### Default Credentials

When using the included seed file (`seeds/1.json`), the following accounts are available:

- **Wizard Account**:
  - Email: `wizard@yourhost.com`
  - Password: `wizard`
  - Characters: Wizard (Admin), Architect, Builder

- **Programmer Account**:
  - Email: `programmer@yourhost.com`
  - Password: `programmer`
  - Character: Programmer

---

## Project Structure

### Directory Structure

```
.run/
  moomp deploy.run.xml
  telnet server.run.xml
commands/
  text/
    __init__.py
    base.py
    build.py
    copy.py
    describe.py
    dig.py
    hide.py
    logout.py
    look.py
    move.py
    register.py
    rename.py
    say.py
    take.py
    warp.py
    waypoint.py
consumers/
  __init__.py
  base.py
  properties.py
  room.py
  script.py
  speech.py
docker/
  mosquitto/
    mosquitto.conf
  entrypoint.sh
entrypoints/
  llm.py
  mqtt.py
  seed.py
  telnet.py
middleware/
  updater.py
migrations/
  __init__.py
  m000000001.py
  m000000002.py
models/
  __init__.py
  account.py
  character.py
  events.py
  instance.py
  object.py
  portal.py
  roles.py
  room.py
  script.py
  speech.py
seeds/
  1.json
services/
  telnet/
    auth_n.py
    input.py
    mqtt.py
    telnet.py
  account.py
  authn.py
  character_test.py
  character.py
  instance.py
  mqtt.py
  object_test.py
  object.py
  portal_test.py
  portal.py
  room_test.py
  room.py
  script.py
  session.py
templates/
  character/
    character.templ
    text.py
    welcome.templ
  object/
    object.templ
    text.py
  portal/
    portal.templ
    text.py
  room/
    room.templ
    text.py
  utils/
    authn/
      authn.json
      authn.py
      config.py
    text/
      color.py
      config.py
      graphics.py
      style.py
      text.json
      text.py
  text.py
utils/
  clean.py
  color.py
  db.py
  migrate.py
  system.py
  types.py
.env.deploy
.env.example
.gitignore
.python-version
docker-compose.deploy.yml
docker-compose.yml
Dockerfile
LICENSE
main.py
pyproject.toml
README.md
```

### Entrypoints

The main entry point is `main.py`, which provides a command-line interface with the following sub-commands:

- **telnet**: Start the Telnet server
- **mqtt**: Start the MQTT consumer
- **seed**: Seed the database with initial data
- **llm**: Start the LLM integration service

### Key Components

#### Commands (`commands/`)
Text-based commands that players can execute:
- **Movement**: `move`, `warp`, `waypoint`
- **World Building**: `build`, `dig`, `describe`, `hide`, `rename`
- **Object Management**: `copy`, `take`
- **Communication**: `say`
- **Information**: `look`
- **Account**: `register`, `logout`

#### Consumers (`consumers/`)
MQTT message consumers for handling real-time events:
- **Room Consumer**: Handles room-related events (entries, exits)
- **Script Consumer**: Executes Lua scripts in response to events
- **Speech Consumer**: Processes chat and communication
- **Properties Consumer**: Manages dynamic object properties

#### Models (`models/`)
MongoEngine document models representing core entities:
- **Account**: User accounts with authentication
- **Character**: Player characters with inventory and properties
- **Room**: Virtual locations with descriptions
- **Portal**: Connections between rooms
- **Object**: Items that can be manipulated
- **Script**: Lua scripts attached to game entities
- **Instance**: Game world instances
- **Role**: Permission roles
- **Events**: Audit log of system events
- **Speech**: Communication messages

#### Services (`services/`)
Business logic layer:
- **Authentication**: Account and character authentication
- **Character Management**: Character CRUD operations
- **Room Management**: Room creation and navigation
- **Object Management**: Object manipulation
- **Portal Management**: Connection management
- **MQTT Service**: Message broker integration
- **Script Service**: Lua script execution
- **Session Management**: Player session handling

#### Templates (`templates/`)
Cheetah3 templates for rendering game output:
- **Character Templates**: Player information displays
- **Room Templates**: Room descriptions
- **Object Templates**: Item descriptions
- **Portal Templates**: Exit descriptions
- **Text Utilities**: Color, graphics, and styling helpers

#### Middleware (`middleware/`)
Request/response processing:
- **Updater**: MQTT event publishing and topic management

#### Migrations (`migrations/`)
Database migration scripts for schema updates

---

## Included Packages and Dependencies

### Core Dependencies

- **mongoengine** (^0.29.1): MongoDB object-document mapper
- **pydantic** (^2.7.4): Data validation using Python type annotations
- **paho-mqtt** (^2.1.0): MQTT client library
- **telnetlib3** (^2.0.4): Telnet server implementation
- **bcrypt** (^4.2.0): Password hashing
- **lupa** (^2.2): Lua integration for Python
- **cheetah3** (^3.2.6.post1): Template engine
- **email-validator** (^2.2.0): Email validation

### AI/ML Integration

- **langchain** (^0.3.23): LLM framework
- **langchain-openai** (^0.3.14): OpenAI integration
- **langchain-ollama** (^0.3.2): Ollama integration
- **ollama** (^0.4.8): Ollama client

### Utilities

- **argparse** (^1.4.0): Command-line argument parsing
- **blinker** (^1.8.2): Signal/event dispatching
- **pluralizer** (^1.2.0): Text pluralization
- **ansi-escapes** (^0.1.1): ANSI terminal control
- **pydantic-extra-types** (^2.9.0): Additional Pydantic field types

### Development Dependencies

- **black** (^24.10.0): Code formatter
- **pytest-env** (^1.1.3): Test environment configuration
- **prettier** (^0.0.7): Code formatting

---

## Try It Online

Connect to the public demo server:

```bash
telnet moomp.robbiebyrd.com 7890
```

**Demo Account**: `wizard@yourhost.com` / `wizard`

---

For more information, visit the [GitHub repository](https://github.com/robbiebyrd/moomp.git).
