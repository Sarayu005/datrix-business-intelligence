# AI Development Notes — Datrix

## 1. AI Tools Used

- **ChatGPT:** Used as a development assistant to help plan the application, troubleshoot implementation issues, improve code structure, and understand backend, database, and testing concepts.
- **Google Gemini API:** Integrated into the application to interpret natural-language business questions and support AI-powered analytics responses.
- **VS Code:** Used as the primary development environment.

## 2. How AI Was Used During Development

AI assistance was used to explore implementation approaches, understand errors, and improve the organization of the application. I reviewed and tested the resulting code as part of development rather than treating AI-generated suggestions as automatically correct.

Within Datrix, the Gemini integration helps interpret questions about business data. The backend connects the interpreted question to the relevant analytics functionality and returns a response with supporting evidence where available.

## 3. Problems Encountered

- **Data quality:** Some transaction records could not safely contribute to revenue calculations because of data-quality issues or eligibility rules.
- **Natural-language interpretation:** Business questions need to be mapped to supported analytics operations and parameters, such as the months being compared.
- **Integration and debugging:** The frontend, FastAPI backend, database, and AI service needed to work together correctly.
- **Environment and deployment setup:** The application requires appropriate Python dependencies and secure configuration of the Gemini API key.

## 4. How I Debugged the Problems

- Inspected data-loading and validation logic to understand which records were eligible for revenue calculations.
- Tested analytics functions and API endpoints independently.
- Used automated API tests to check expected responses and invalid or unsupported inputs.
- Checked application errors and terminal output while integrating the frontend and backend.
- Kept API credentials in environment configuration rather than embedding them in source code.

## 5. What I Would Improve With Another Day

- Add more unit and integration tests, especially for edge cases in data validation and AI question interpretation.
- Improve error handling for API failures, malformed AI responses, and missing configuration.
- Expand supported natural-language questions and improve validation of interpreted parameters.
- Add more detailed documentation, dashboard screenshots, and reproducible setup instructions.
- Review security, logging, and performance before deploying the application for wider use.

## Conclusion

Datrix demonstrates how a Python-based analytics backend, relational database, interactive dashboard, and AI-powered question interface can be combined into a business intelligence application. The next improvements would focus on reliability, test coverage, and maintainability.
