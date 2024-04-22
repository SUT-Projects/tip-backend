## TIP Backend

## Prerequisites
List of prerequisites required to run the project are listed below:
- Install **Git** form [git-scm.com](https://git-scm.com/downloads) (if not installed)
- Install **python** from [python.org](https://www.python.org/downloads/) (if not installed)
- Install **mongoDB** from [mongodb.org](https://www.mongodb.com/try/download/community) (if not installed)


## Installation
Cloning a Python project from GitHub and getting it up and running on your system is a common task for developers. Here are the steps:

### 1. Clone the Repository
Open your terminal or command prompt and navigate to the directory where you want to store the project. Then, use the `git clone` command followed by the URL of the GitHub repository. For example:
```bash
git clone https://github.com/SUT-Projects/tip-backend.git
```

### 2. Navigate to the Project Directory
Once the repository is cloned, navigate into the project directory using the cd command:
```bash
cd tip-backend
```

### 3. Set Up a Virtual Environment (Optional but Recommended)
It's a good practice to use virtual environments to isolate project dependencies. You can create a **virtual environment** using `venv` or `virtualenv`. First, ensure you have venv installed by running:
```bash
python3 -m venv venv
```
Activate the virtual environment:
- on **WINDOWS**
```bash
  venv\Scripts\activate
```
- on **MacOS** or **Unix**
```bash
  source venv/bin/activate
```

### 4. Install Dependencies
With the virtual environment activated, you can install the project dependencies using pip. Usually, there's a requirements.txt file listing all dependencies. Run:
```bash
pip install -r requirements.txt
```