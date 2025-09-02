# DrQuery ⚡

**Intelligent Database Query Assistant**

Created by **Vaibhav Nagre**

## 🚀 Live Demo
[**Try DrQuery →**](https://drquery.streamlit.app) *(Coming Soon)*

## 📖 Overview

DrQuery is an intelligent database query assistant that transforms natural language into SQL queries. Built with modern AI technology and a beautiful ocean-themed interface.

## ✨ Features

- **💬 Natural Language Chat**: Query your database using plain English
- **📊 Smart Visualizations**: AI-powered chart generation from your data  
- **🛠️ Query Builder**: Visual SQL query construction and editing
- **🎨 Modern UI**: Professional ocean-themed design
- **⚡ Fast & Responsive**: Built with Streamlit for optimal performance

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **AI Engine**: LangChain + Groq (Llama 3.1)
- **Database**: MySQL connector
- **Visualizations**: Plotly
- **Deployment**: Streamlit Community Cloud

## 📦 Installation

### Option 1: Quick Start (Recommended)
```bash
git clone https://github.com/vaibhav-nagre/DrQuery.git
cd DrQuery
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Option 2: Local Development
```bash
git clone https://github.com/vaibhav-nagre/DrQuery.git
cd DrQuery
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/main.py
```

## ⚙️ Configuration

1. **Create a `.env` file** in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

2. **Get your Groq API key**:
   - Visit [Groq Console](https://console.groq.com/)
   - Create an account and generate an API key
   - Add it to your `.env` file

## 🚀 Usage

1. **Launch the application**
2. **Connect to your database** using the sidebar
3. **Choose your preferred mode**:
   - **Chat**: Ask questions in natural language
   - **Visualization**: Generate charts and graphs
   - **Query Builder**: Build and edit SQL queries

## 🎨 Features Showcase

### Natural Language Queries
```
"Show me all patients who had appointments this month"
"What's the average age of patients by department?"
"Find the top 5 doctors with the most appointments"
```

### Smart Visualizations
- Automatic chart type detection
- Interactive Plotly charts
- Export capabilities
- Data insights generation

### Query Builder
- Visual SQL construction
- Real-time query optimization
- Performance estimation
- Query execution and editing

## � Deployment

### Streamlit Community Cloud
1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy from your forked repository
4. Add your `GROQ_API_KEY` in the Streamlit Cloud secrets

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍� Creator

**Vaibhav Nagre**
- GitHub: [@vaibhav-nagre](https://github.com/vaibhav-nagre)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.com/) and [Groq](https://groq.com/)
- Visualizations by [Plotly](https://plotly.com/)

---

⭐ **Star this repository if you find it helpful!**

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
