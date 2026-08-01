# General AI Rules

1. **Context Awareness**: 
   Before making any changes or proposing architectural decisions, ALWAYS read the following context files to ensure alignment with the project. You can find them in the `.agents/` directory:
   - `product.md`: To understand the project's goals.
   - `structure.md`: To understand the folder layout and domain-driven design structure.
   - `tech.md`: To ensure you are using the correct libraries and tools.
   - `workflow.md`: To understand the data flow and system architecture.

2. **Living Documentation**:
   When you create new files, add new dependencies, change the architecture/flow, or introduce new structural concepts, you MUST update the corresponding context files:
   - Update `product.md` if the product scope, core objectives, or features change.
   - Update `structure.md` if you create new important files or folders, or restructure the app.
   - Update `tech.md` if you introduce new libraries, frameworks, or dependencies.
   - Update `workflow.md` if the execution flow, system interactions, or sequence of operations changes.

3. **Tech Stack Constraints**:
   Stick to the tech stack defined in `tech.md`. Do not introduce new frameworks or swap existing ones (e.g., do not switch from FastAPI to Flask or Celery to RQ) without explicit user permission.
