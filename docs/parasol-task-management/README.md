# Parasol Task Management System

## Overview

A comprehensive task management system built using the Parasol DDD Framework integrated with Amplifier's Document-Driven Development workflow. The system demonstrates value-driven development from strategic capabilities to operational implementation.

## Architecture

### Clean/Hexagonal Hybrid Architecture

The system uses a hybrid of Clean Architecture and Hexagonal Architecture patterns, aligned with Parasol's hierarchical capability structure:

```
┌──────────────────────────────────────────┐
│          Presentation Layer              │
│         (UI Components, Pages)           │
├──────────────────────────────────────────┤
│          Application Layer               │
│      (Use Cases, L2 Capabilities)       │
├──────────────────────────────────────────┤
│            Domain Layer                  │
│   (Entities, Services, L3 Operations)   │
├──────────────────────────────────────────┤
│         Infrastructure Layer            │
│    (Database, External Services)        │
└──────────────────────────────────────────┘
```

## Core Features

### Task Management
- Create, read, update, and delete tasks
- Rich task attributes (title, description, priority, status, due date)
- Task templates for common workflows
- Bulk operations support

### Assignment & Collaboration
- Assign tasks to team members
- Reassign and delegate capabilities
- Comment threads on tasks
- @mentions and notifications

### Progress Tracking
- Real-time progress visualization
- Burndown charts and velocity tracking
- Custom dashboards
- Automated status updates

### Analytics & Reporting
- Comprehensive metrics dashboard
- Custom report generation
- Predictive completion dates
- Resource utilization analysis

## Capability Hierarchy

### L1: Strategic Capabilities
- **Project Success Capability**: Ensure successful project delivery

### L2: Tactical Capabilities
- **Task Management Capability**: Manage tasks efficiently
- **Resource Optimization Capability**: Optimize team resources
- **Progress Tracking Capability**: Track and report progress

### L3: Operational Capabilities
- **Task CRUD Operations**: Basic task operations
- **Task Assignment Operations**: Assignment and delegation
- **Progress Analytics Operations**: Metrics and reporting

## API Reference

### REST Endpoints

#### Tasks
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/:id` - Get task details
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

#### Assignments
- `POST /api/tasks/:id/assign` - Assign task
- `PUT /api/tasks/:id/reassign` - Reassign task
- `POST /api/tasks/bulk-assign` - Bulk assignment

#### Analytics
- `GET /api/analytics/metrics` - Get metrics
- `POST /api/analytics/reports` - Generate report
- `GET /api/analytics/predictions` - Get predictions

## Domain Model

### Core Entities

#### Task
```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: Priority;
  assigneeId: string;
  projectId: string;
  dueDate: Date;
  createdAt: Date;
  updatedAt: Date;

  // Parasol extensions
  capabilityLink: string;
  valueImpact: number;
  metrics: TaskMetrics;
}
```

#### User
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  capabilities: string[];
  teamId: string;
}
```

#### Project
```typescript
interface Project {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  ownerId: string;
  startDate: Date;
  endDate: Date;

  // Parasol extensions
  valueProposition: string;
  kpis: KPI[];
  capabilities: string[];
}
```

### Value Objects

#### TaskStatus
```typescript
enum TaskStatus {
  TODO = 'TODO',
  IN_PROGRESS = 'IN_PROGRESS',
  IN_REVIEW = 'IN_REVIEW',
  BLOCKED = 'BLOCKED',
  DONE = 'DONE',
  CANCELLED = 'CANCELLED'
}
```

#### Priority
```typescript
enum Priority {
  CRITICAL = 'CRITICAL',
  HIGH = 'HIGH',
  MEDIUM = 'MEDIUM',
  LOW = 'LOW'
}
```

## Getting Started

### Prerequisites
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourorg/parasol-task-management.git
cd parasol-task-management

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
npm run db:migrate

# Seed initial data
npm run db:seed

# Start development server
npm run dev
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:3000
```

## Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/taskdb

# Redis
REDIS_URL=redis://localhost:6379

# Application
PORT=3000
NODE_ENV=development

# Auth
JWT_SECRET=your-secret-key
JWT_EXPIRY=7d

# Parasol Configuration
PARASOL_KNOWLEDGE_DB=./knowledge.db
PARASOL_PATTERN_PATH=./patterns
```

## Testing

### Unit Tests
```bash
npm run test:unit
```

### Integration Tests
```bash
npm run test:integration
```

### End-to-End Tests
```bash
npm run test:e2e
```

### Coverage Report
```bash
npm run test:coverage
```

## Deployment

### Production Build
```bash
npm run build
npm start
```

### Kubernetes Deployment
```bash
kubectl apply -f k8s/
```

## Metrics & Monitoring

### Key Metrics
- Task completion rate
- Average cycle time
- Team utilization
- System performance

### Monitoring Stack
- Prometheus for metrics collection
- Grafana for visualization
- ELK stack for logging
- Sentry for error tracking

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- Documentation: [docs.parasol-tasks.com](https://docs.parasol-tasks.com)
- Issues: [GitHub Issues](https://github.com/yourorg/parasol-task-management/issues)
- Discord: [Join our community](https://discord.gg/parasol)

---

*Built with Parasol DDD Framework and Amplifier's Document-Driven Development*