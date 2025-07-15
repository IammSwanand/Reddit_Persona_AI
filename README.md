# Reddit Persona AI

An AI-powered Reddit user persona analyzer that generates comprehensive psychological profiles and business insights using GROQ's Llama 3 70B model.

**IMPORTANT - Create a .env file in your system after pulling this Repo**

**Get GROQ API key here - https://console.groq.com/keys**

**Also if first time if the code throws "invalid API key" error then create another API key from the same link and it'll work for sure.**

## 📁 Project Structure

```
Reddit_Persona_AI/
├── Hungry_Move_Persona.txt     # Sample analysis of u/Hungry-Move-6603
├── kojied_persona.txt          # Sample analysis of u/kojied
├── README.md                   # This file
├── requirements.txt             # Python dependencies
└── script.py                    # Main executable script

```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a .env file and add GROQ API Key**
   ```.env
   GROQ_API_KEY=your_api_key_here
   ```

3. **Run the script:**
   ```bash
   py script.py
   ```

4. **Follow the interactive prompts:**
5. ```bash
   - Enter Reddit username or profile URL
   - Choose output filename (or press Enter for auto-generated)
   - Set data analysis limit (default: 1000 posts/comments)
   ```

## 🎯 Features

- **AI-Powered Analysis**: Uses GROQ's Llama 3 70B for advanced persona generation
- **Interactive Interface**: User-friendly command-line prompts
- **Flexible Input**: Accepts various Reddit URL formats or just usernames
- **Comprehensive Profiling**: Generates detailed psychological and behavioral analysis
- **Evidence-Based**: All insights backed by specific posts/comments
- **Configurable Limits**: Adjustable data collection limits (up to 3000+ items)
- **Auto-Generated Filenames**: Automatic timestamped output files
- **Error Handling**: Robust handling of network issues and invalid inputs

## 📊 Sample Users

The repository includes pre-generated analyses for:
- **kojied**: Active NYC-based tech professional with gaming interests
- **Hungry-Move-6603**: User with different activity patterns

## 🔍 Analysis Output

Each generated persona includes:

1. **Basic Information**: Age estimates, location, occupation
2. **Personality Traits**: Analytical, curious, helpful, etc. with confidence levels
3. **Interests and Hobbies**: Gaming, technology, food, anime, etc.
4. **Communication Style**: Informed, concise, helpful patterns
5. **Demographic Indicators**: Education level, income estimates
6. **Behavioral Patterns**: Online presence, learning tendencies
7. **Values and Beliefs**: Self-care, fairness, equality concerns
8. **Motivations and Goals**: Personal growth, social connections
9. **Frustrations and Pain Points**: Game mechanics, workplace fairness
10. **Business/Marketing Insights**: Target audience, marketing strategies

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **AI Model**: GROQ Llama 3 70B (llama3-70b-8192)
- **Data Source**: Reddit JSON API
- **Dependencies**: requests, groq, python-dotenv
- **Code Style**: PEP-8 compliant with type hints
- **Security**: Environment variables for API key management

## 💡 How It Works

1. **Input Processing**: Normalizes various Reddit URL formats
2. **Data Collection**: Scrapes posts and comments using pagination
3. **AI Analysis**: Sends structured prompt to GROQ for persona generation
4. **Output Generation**: Creates formatted text file with analysis
5. **Evidence Tracking**: Maintains links to original posts/comments

## 🔧 Usage Examples

```bash
# Basic usage
py script.py

# Example interaction:
Enter Reddit profile information:
Reddit Profile: kojied

Choose output filename:
Output filename: [Press Enter for auto-generated]

Data analysis limit:
Max items (or press Enter for 1000): [Press Enter]
```

## 📈 Performance

- **Data Fetching**: ~1-2 seconds per 100 items
- **AI Analysis**: 1-3 minutes for comprehensive persona
- **Total Runtime**: 2-5 minutes for typical user analysis
- **Rate Limiting**: Built-in delays to respect Reddit's API limits

## 🛡️ Privacy & Security

- **Public Data Only**: Analyzes only publicly available Reddit content
- **API Key Protection**: Uses .env file (excluded from version control)
- **No Data Storage**: Doesn't permanently store personal information
- **Ethical Guidelines**: Intended for research and educational purposes

## 🚨 Error Handling

The script handles:
- Invalid Reddit URLs or usernames
- Private or deleted accounts
- Network connectivity issues
- API rate limiting
- Missing or corrupted data
- Invalid user input

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- GROQ API key (provided for evaluation)
- Valid Reddit usernames (public profiles only)

## 🔄 Sample Output Format

```
=== AI-POWERED REDDIT PERSONA ANALYSIS ===
Username: kojied
Generated: 2025-07-15 18:13:20
Total Posts Analyzed: 31
Total Comments Analyzed: 328

**Persona Analysis: kojied**

**1. Basic Information**
* Age: Late 20s to early 30s
* Location: New York City, USA
* Occupation: Software developer or tech professional

[Additional analysis sections...]

=== ANALYSIS COMPLETED ===
Powered by GROQ AI (Llama 3 70B)
```

## 📞 Support

For questions or issues:
1. Check that your .env file contains a valid GROQ API key
2. Verify internet connectivity
3. Ensure the Reddit username is valid and public
4. Review error messages for specific guidance

---

**Note**: This project demonstrates AI-powered user analysis capabilities. Please use responsibly and respect user privacy.
