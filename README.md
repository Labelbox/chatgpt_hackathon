# Challenge

  - You’re tasked with fine-tuning ChatGPT with a specific goal - sentiment analysis in Reddit posts
  - …but you have a limited budget for model training 
  - Due to this constraint, you can only fine-tune ChatGPT **three times**, each time you only get 2000 incremental training data rows
    - So, you can train on 2000 data rows in Round 1, 4000 data rows in Round 2, and 6000 data rows in Round 3
    

# How to Enter

  - Create teams of three with a unique team name - provide your .edu email to your professor and we will create Labelbox accounts for you and your team in the hackathon workspace
  - Follow the notebooks in this repo to register, send curated data rows to a model run, and fine tune ChatGPT on curated data rows
  
# Key Steps
  - Register your team in Labelbox with the `Register Your Team` notebook once you have Labelbox accounts
  - Using the Labelbox Catalog, curate a Round 1 training set by batching selected data rows to your team's Labelbox Project
  - Once you're happy with your 2000 data rows in your team's Labelbox Project, run the `Send Curated Data Rows to Model Run` notebook
  - Review your annotations one more time in your team's Model Run, if you're unhappy with your Model Run prior to fine-tuning, you can delete it and refine data row selection in your team's Labelbox Project
    - **Once you've fine-tuned your model and created predictions, you cannot delete the model run**
  - Once you're happy with your team's Model Run selection, run the `Fine-Tune ChatGPT based on Data Rows in Model Run` to create predictions and upload them to Labelbox
  - Review model performance using the _metrics_ tab in Labelbox and begin curating your next 2000 data rows to send to your team's Labelbox Project
  - Repeat for rounds 2 and 3, each time creating an entirely new Model Run in your team's Labelbox Model

# Notebooks

|            Notebook            |  Github  |    Google Colab   |
| ------------------------------ | -------- | ----------------- |
| Register Your Team            | [![Github](https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white)](notebooks/register.ipynb)  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1lKEENBtcj4vVzuWmYtX_qaRplbxI9TGf) |
| Send Curated Data Rows to Model Run        | [![Github](https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white)](notebooks/model-run.ipynb)  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1JHlGlkLlVeL0mXmBrpp9z423vkdTYr5W) |
| Fine-Tune ChatGPT based on Data Rows in Model Run     | [![Github](https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white)](notebooks/fine-tune.ipynb)  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Vg-D0b3Jif8oBW4LF4ksVdnLA4JpshfP) |
------
    
  
