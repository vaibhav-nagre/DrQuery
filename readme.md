# DrQuery ⚡

**AI-Powered Database Query Assistant with Premium Web Interface**

DrQuery is an intelligent database query tool that transforms natural language questions into SQL queries using advanced AI. Built with a modern Streamlit interface, it provides an intuitive chat-based experience for database exploration and analysis.

## ✨ Features

- 🤖 **AI-Powered SQL Generation** - Convert natural language to SQL using OpenAI and Groq models
- 💬 **Chat Interface** - Interactive conversation-based database querying
- 📊 **Data Visualization** - Built-in charts and visualizations using Plotly
- 🔍 **Query Insights** - Performance analysis and optimization suggestions
- 🎨 **Premium UI/UX** - Modern, responsive interface with custom styling
- 🗄️ **Multi-Database Support** - MySQL and PostgreSQL compatibility
- 📈 **Real-time Results** - Instant query execution and result display

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MySQL or PostgreSQL database
- OpenAI API key or Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vaibhav-nagre/dr_query.git
   cd dr_query
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   # OR
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Launch the application**
   ```bash
   python app.py
   ```

The application will start automatically and open in your default browser.

## 🛠️ Configuration

### Database Connection

Configure your database connection through the sidebar in the web interface:

- **Host**: Database server address
- **Port**: Database port (default: 3306 for MySQL)
- **Database**: Database name
- **Username**: Database username
- **Password**: Database password

### AI Model Selection

Choose between:
- **OpenAI GPT models** (requires OpenAI API key)
- **Groq models** (requires Groq API key)

## 💡 Usage Examples

### Natural Language Queries

```
"Show me all customers from New York"
"What are the top 5 selling products this month?"
"Find all orders placed in the last 30 days"
"Calculate the average order value by customer segment"
```

### Features in Action

1. **Connect to Database** - Use the sidebar to establish connection
2. **Ask Questions** - Type natural language questions in the chat
3. **View Results** - See formatted results with automatic visualizations
4. **Analyze Performance** - Get query insights and optimization tips

## 📁 Project Structure

```
drquery/
├── app.py                    # Main launcher
├── requirements.txt          # Dependencies
├── src/
│   ├── app_premium.py       # Premium Streamlit application
│   ├── components/          # UI components
│   │   ├── chat_interface.py
│   │   ├── result_display.py
│   │   └── sidebar.py
│   ├── styles/
│   │   └── main.css         # Custom styling
│   └── utils/
│       └── database.py      # Database utilities and AI chains
├── database/
│   ├── schema.sql           # Sample database schema
│   └── sample_data.sql      # Sample data
└── docs/                    # Documentation
```

## 🔧 Development

### Running Tests

```bash
pytest
```

### Custom Styling

Modify `src/styles/main.css` to customize the appearance of the application.

### Adding New Features

The modular structure allows easy extension:
- Add new UI components in `src/components/`
- Extend database functionality in `src/utils/database.py`
- Customize styling in `src/styles/main.css`

## 📊 Version History

- **v3.0.0** - Premium chat interface with enhanced AI integration
- **v2.0.0** - Visual interface with drag-and-drop query builder
- **v1.1.0** - Query optimization and performance analysis
- **v1.0.0** - Initial CLI-based SQL query builder

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- **LangChain** for the AI framework
- **Streamlit** for the web interface
- **OpenAI** and **Groq** for AI models
- **Plotly** for data visualizations

---

**Made with ❤️ by [Vaibhav Nagre](https://github.com/vaibhav-nagre)**
