# client_webui/client_webui/README.md

# Client Web UI

This project is a web application built using LitElement, esbuild, and Tailwind CSS. It serves as a client interface for interacting with a camera feed and related functionalities.

## Project Structure

```
client_webui
├── src
│   ├── components
│   │   ├── app-root.ts        # Main application component
│   │   └── camera-view.ts     # Component for displaying camera feed
│   ├── styles
│   │   ├── tailwind.css       # Tailwind CSS styles
│   │   └── theme.css          # Custom theme styles
│   ├── utils
│   │   └── api.ts             # API utility functions
│   └── index.ts               # Entry point of the application
├── public
│   ├── index.html             # Main HTML file
│   └── favicon.svg            # Favicon for the application
├── esbuild.config.js          # Configuration for esbuild
├── package.json               # npm configuration file
├── tailwind.config.js         # Tailwind CSS configuration
├── tsconfig.json              # TypeScript configuration
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd client_webui
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Build the project:**
   ```
   npm run build
   ```

4. **Run the development server:**
   ```
   npm start
   ```

## Usage

- Open your browser and navigate to `http://localhost:3000` to view the application.
- The main application component (`AppRoot`) will render the camera view and any related controls.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.