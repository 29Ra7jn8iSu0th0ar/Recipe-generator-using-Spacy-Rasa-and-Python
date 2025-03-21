#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().system('mkdir recipe_bot')


# In[7]:


get_ipython().run_line_magic('cd', 'recipe_bot')


# In[ ]:


# upper vaala code Rasa ka base project structure create karega:

# data/ → Training data
# models/ → Trained model
# actions/ → Custom Python actions
# domain.yml → Bot ka response logic
# config.yml → NLU pipeline & policies
# nlu.yml → Intent aur examples
# stories.yml → Conversation flow
# rules.yml → Bot ke rules


# In[8]:


get_ipython().system('pip install SQLAlchemy==1.4.49')


# In[9]:


# Force UTF-8 encoding in Jupyter
get_ipython().run_line_magic('env', 'PYTHONUTF8=1')


# In[10]:


get_ipython().system('rasa init --no-prompt')


# In[11]:


get_ipython().system('pip install SQLAlchemy==1.4.49')


# In[12]:


import os

# Create 'data' folder if it doesn't exist
os.makedirs('data', exist_ok=True)


# In[13]:


get_ipython().run_cell_magic('writefile', 'data/nlu.yml', 'version: "3.1"\nnlu:\n- intent: greet\n  examples: |\n    - hello\n    - hi\n    - hey\n    - good morning\n    - what\'s up\n\n- intent: goodbye\n  examples: |\n    - bye\n    - see you later\n    - goodbye\n    - take care\n\n- intent: ask_recipe\n  examples: |\n    - Can you give me a recipe for pasta?\n    - I want to cook biryani, do you have a recipe?\n    - Suggest me a recipe with chicken\n    - How do I make a smoothie?\n    - Give me a dessert recipe\n')


# In[14]:


get_ipython().run_cell_magic('writefile', 'data/stories.yml', 'version: "3.1"\nstories:\n- story: ask for a recipe\n  steps:\n  - intent: greet\n  - action: utter_greet\n\n- story: ask for recipe and respond\n  steps:\n  - intent: ask_recipe\n  - action: action_provide_recipe\n\n- story: end conversation\n  steps:\n  - intent: goodbye\n  - action: utter_goodbye\n')


# In[15]:


get_ipython().run_cell_magic('writefile', 'domain.yml', 'version: "3.1"\nintents:\n  - greet\n  - goodbye\n  - ask_recipe\n\nresponses:\n  utter_greet:\n    - text: "Hello! What recipe are you looking for today?"\n    - text: "Hi! Do you have any particular dish in mind?"\n\n  utter_goodbye:\n    - text: "Goodbye! Happy cooking!"\n    - text: "See you next time with more recipes!"\n\nactions:\n  - action_provide_recipe\n')


# In[16]:


import os

# Create 'actions' folder if it doesn't exist
os.makedirs('actions', exist_ok=True)


# In[17]:


get_ipython().run_cell_magic('writefile', 'actions/actions.py', 'from typing import Any, Text, Dict, List\nfrom rasa_sdk import Action, Tracker\nfrom rasa_sdk.executor import CollectingDispatcher\nimport random\n\nclass ActionProvideRecipe(Action):\n\n    def name(self) -> Text:\n        return "action_provide_recipe"\n\n    def run(self, dispatcher: CollectingDispatcher,\n            tracker: Tracker,\n            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:\n\n        recipes = {\n            "pasta": "Boil pasta, add sauce, and cook with cheese.",\n            "biryani": "Marinate chicken, cook with rice and spices.",\n            "smoothie": "Blend banana, berries, and milk.",\n            "omelette": "Beat eggs, add salt, cook with butter.",\n            "salad": "Mix lettuce, tomato, cucumber, and dressing."\n        }\n\n        user_message = tracker.latest_message.get(\'text\').lower()\n        \n        selected_recipe = None\n        for dish, recipe in recipes.items():\n            if dish in user_message:\n                selected_recipe = recipe\n                break\n\n        if selected_recipe:\n            dispatcher.utter_message(text=f"Here is the recipe: {selected_recipe}")\n        else:\n            dispatcher.utter_message(text="Sorry, I don\'t have that recipe yet. Try asking for pasta, biryani, smoothie, omelette, or salad.")\n\n        return []\n')


# In[18]:


get_ipython().run_cell_magic('writefile', 'endpoints.yml', 'action_endpoint:\n  url: "http://localhost:5055/webhook"\n')


# In[19]:


# Ensure you are in the correct directory
import os

# Create config.yml file
config_content = """
version: "3.1"

# NLU pipeline configuration
pipeline:
- name: WhitespaceTokenizer
- name: CountVectorsFeaturizer
- name: DIETClassifier
  epochs: 100
  constrain_similarities: true
- name: EntitySynonymMapper
- name: ResponseSelector
  epochs: 100
- name: FallbackClassifier
  threshold: 0.3
  ambiguity_threshold: 0.1

# Policies for dialogue management
policies:
- name: MemoizationPolicy
- name: RulePolicy
- name: TEDPolicy
  max_history: 5
  epochs: 100
"""

# Write to config.yml
with open("config.yml", "w") as f:
    f.write(config_content)

print("config.yml file created successfully!")


# In[20]:


import os
print("Current Working Directory:", os.getcwd())


# In[21]:


# List all files and folders in the current directory
import os

# Function to display the folder structure
def list_files(startpath='.'):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

# Display the folder structure
list_files()


# In[22]:


# Create credentials.yml with default content
credentials_content = """
# This file contains the credentials for external connectors.
# You can find more information in the documentation:
# https://rasa.com/docs/rasa/messaging-and-voice-channels

rest:
  # you don't need to provide anything here - this channel is enabled by default
  # to send messages to Rasa using:
  # POST http://localhost:5005/webhooks/rest/webhook

# facebook:
#   verify: "YOUR_VERIFY_TOKEN"
#   secret: "YOUR_APP_SECRET"
#   page-access-token: "YOUR_PAGE_ACCESS_TOKEN"

# slack:
#   slack_token: "YOUR_SLACK_TOKEN"
#   slack_channel: "YOUR_SLACK_CHANNEL"
#   slack_signing_secret: "YOUR_SLACK_SIGNING_SECRET"

# socketio:
#   user_message_evt: "user_uttered"
#   bot_message_evt: "bot_uttered"
#   session_persistence: true

# telegram:
#   access_token: "YOUR_TELEGRAM_ACCESS_TOKEN"
"""

# Write the content to credentials.yml
with open("credentials.yml", "w", encoding="utf-8") as file:
    file.write(credentials_content)

print(" credentials.yml created successfully!")


# In[23]:


list_files()


# In[24]:


# Update the config.yml with the missing language parameter
config_content = """
# Configuration for Rasa NLU.
# https://rasa.com/docs/rasa/nlu/components/

language: en  # <-- Add this line to specify the language (English)

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: DIETClassifier
    epochs: 100
  - name: EntitySynonymMapper

# Configuration for Rasa Core.
# https://rasa.com/docs/rasa/core/policies/

policies:
  - name: MemoizationPolicy
  - name: RulePolicy
  - name: TEDPolicy
    max_history: 5
    epochs: 100
"""

# Write the content to config.yml
with open("config.yml", "w", encoding="utf-8") as file:
    file.write(config_content)

print("config.yml updated successfully!")


# In[25]:


# Display config.yml content
with open("config.yml", "r", encoding="utf-8") as file:
    print(file.read())


# In[26]:


get_ipython().system('rasa train')


# In[ ]:


get_ipython().system('rasa run')


# In[ ]:




