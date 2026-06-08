# Coral Image Identifier - Frontend

This is a React-based web application built with [Vite](https://vitejs.dev/) and [React Flow](https://reactflow.dev/) to interact with the Coral Image Identifier API.

## 🚀 Getting Started

### 1. Start the Backend
Before running the frontend, ensure your Python API is running:
```bash
# From the project root
python src/api/server.py
```
The API will be available at `http://localhost:8000`.

### 2. Run the Frontend
```bash
cd frontend
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🛠️ Tech Stack
- **React**: UI Library
- **React Flow**: Node-based visualization
- **Tailwind CSS**: Styling
- **Axios**: API requests
- **Lucide React**: Icons

## 🧩 Pipeline Nodes
1. **Upload Node**: Select or drag-and-drop a coral image.
2. **ML Model Node**: Visualizes the processing/inference state.
3. **Result Node**: Displays the final coral classification and confidence score.
