# All The Buzz - Frontend

## Overview

All The Buzz is a Vue 3 application built with TypeScript and Vite that provides a content management system for jokes, quotes, trivia, and biographies. The application features user authentication, role-based permissions, and CRUD operations for managing various content types.

## Tech Stack

- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript
- **Build Tool**: Vite
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Styling**: CSS with scoped styles

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── AppHeader.vue   # Navigation header
│   ├── ApproveAndDeny.vue  # Moderation controls
│   ├── Create.vue      # Content creation form
│   ├── DataTable.vue   # Generic table component
│   ├── Delete.vue      # Delete functionality
│   ├── Edit.vue        # Edit functionality
│   ├── Get.vue         # Data fetching and display
│   └── ...
├── views/              # Page components
│   ├── Login.vue       # Authentication page
│   ├── Jokes.vue       # Jokes management
│   ├── Quotes.vue      # Quotes management
│   ├── Trivias.vue     # Trivia management
│   └── Bios.vue        # Biography management
├── router/             # Vue Router configuration
├── utils/              # Utility functions
│   ├── cookies.ts      # Cookie management
│   └── encryption.js   # Encryption utilities
└── assets/             # Static assets and styles
```

## Features

### User Authentication
- Login system with JWT token-based authentication
- Role-based access control (user, manager, admin)
- Secure credential storage using cookies

### Content Management
- **Create**: Add new jokes, quotes, trivia, and bios
- **Read**: Fetch and filter content with various parameters
- **Update**: Edit existing content (write mode)
- **Delete**: Remove content with proper authorization

### Data Display
- Dynamic data tables with customizable columns
- Toggle between read and write modes
- Filter by difficulty, language, and other attributes
- Pagination and search capabilities

### Moderation
- Approve/deny pending content submissions
- Manager-only access to pending items queue
- Real-time table refresh after moderation actions

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Running backend API (see Backend Setup below)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend/All_The_Buzz_Frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

## Backend Setup (Docker)

The frontend requires a running backend API. The backend runs in a Docker container on Linux.

### Prerequisites
- Docker and Docker Compose installed on your system
- Backend source code in the project root directory

### Running the Backend

1. Navigate to the project root directory (Team-White):
```bash
cd Team-White
```

2. Start the backend using Docker Compose:
```bash
docker compose up --build
```

The backend API will be available at `http://localhost:8080`

3. To stop the backend:
```bash
docker compose down
```

### Important Notes for Docker on Linux

- The backend needs to access external authentication services running on the host machine
- Use your host machine's LAN IP address (not `localhost`) in the backend configuration
- Find your LAN IP with: `ip addr | grep inet`
- Ensure the authentication service listens on `0.0.0.0` to accept connections from Docker
- Configure firewall rules to allow connections to required ports

### Environment Variables

Create a `.env` file in the project root directory with:
```
ATLAS_URI=<your-mongodb-connection-string>
JWT_SECRET=<your-jwt-secret>
AUTH_SERVICE_URL=http://<host-lan-ip>:42068
```

## API Configuration

The frontend expects the backend API at `http://localhost:8080`. Update `src/components/*.vue` files if your backend runs on a different host or port.

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (development)
- `http://172.16.0.51:5173` (alternative frontend host)

Add additional origins in the backend CORS configuration if needed.

## Authentication Flow

1. User submits credentials via the Login page
2. Frontend sends credentials to backend proxy endpoint
3. Backend forwards credentials to external authentication service
4. JWT token is returned and stored in encrypted cookies
5. Subsequent API requests include the JWT in the `Bearer` header

## Development Notes

### Type Safety
All components use TypeScript for type safety. Check `tsconfig.json` for compiler options.

### Component Communication
- Parent-child communication uses props and events
- Event emission pattern for table refresh after CRUD operations
- Example: ApproveAndDeny emits `action-complete` event after approval/denial

### State Management
- Local component state using Vue 3 Composition API
- No global state management library (Vuex/Pinia) currently implemented
- Authentication state managed via cookies

## Troubleshooting

### Connection Refused Errors
- Verify backend is running and accessible
- Check backend is listening on correct port
- Ensure CORS is properly configured
- For Docker: verify you're using the correct host IP (not `localhost`)

### Authentication Issues
- Clear browser cookies and try again
- Check JWT expiration
- Verify authentication service is running on the correct port

### Table Not Refreshing
- Ensure components emit proper events after updates
- Check parent component has event handlers configured
- Verify API calls complete successfully

## License

Copyright (C) 2025 Team White
Licensed under the MIT License
