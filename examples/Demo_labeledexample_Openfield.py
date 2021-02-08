#!/usr/bin/env python
# coding: utf-8

# # DeepLabCut Toolbox - Open-Field DEMO
# https://github.com/AlexEMG/DeepLabCut
# 
# #### The notebook accompanies the following user-guide:
# 
# Nath\*, Mathis\* et al. *Using DeepLabCut for markerless pose estimation during behavior across species* Nature Protocols, 2019: https://www.nature.com/articles/s41596-019-0176-0
# 
# This notebook illustrates how to:
# - load the demo project
# - train a network
# - evaluate a network
# - analyze a novel video
# - create an automatically labeled video 
# - plot the trajectories 
# - identify outlier frames
# - annotate the outlier frames manually
# - merge the data sets and update the training set
# - train a network
# 
# Note: This notebook starts from an already initialized project with labeled data.
# 
# 
# The data is a subset from *DeepLabCut: markerless pose estimation of user-defined body parts with deep learning* https://www.nature.com/articles/s41593-018-0209-y (this subset was not used to train models that are shown or evaluated in our paper).

# In[1]:


# Importing the toolbox (takes several seconds)
import deeplabcut


# In[2]:


# Loading example data set:
import os
# Note that parameters of this project can be seen at: *openfield-Pranav-2018-10-30/config.yaml*
from pathlib import Path
path_config_file = os.path.join(os.getcwd(),'openfield-Pranav-2018-10-30/config.yaml')
deeplabcut.load_demo_data(path_config_file)


# In[3]:


#[OPTIONAL] Perhaps plot the labels to see how the frames were annotated:
#(note, this project was created in Linux, so you might have an error in Windows, but this is an optional step)
deeplabcut.check_labels(path_config_file)


# ## Start training of Feature Detectors
# This function trains the network for a specific shuffle of the training dataset. The user can set various parameters in */openfield-Pranav-2018-10-30/dlc-models/.../pose_cfg.yaml*. 
# 
# Training can be stopped at any time. Note that the weights are only stored every 'save_iters' steps. For this demo the state it is advisable to store & display the progress very often. In practice this is inefficient.  

# In[4]:


deeplabcut.train_network(path_config_file, shuffle=1, displayiters=10, saveiters=100)


# **Note, that if it reaches the end or you stop it (by hitting "stop" or by CTRL+C), 
# you will see an "KeyboardInterrupt" error, but you can ignore this!**

# ## Evaluate a trained network
# 
# This function evaluates a trained model for a specific shuffle/shuffles at a particular training state (snapshot) or on all the states. The network is evaluated on the data set (images) and stores the results as .csv file in a subdirectory under **evaluation-results**.
# 
# You can change various parameters in the ```config.yaml``` file of this project. For evaluation all the model descriptors (Task, TrainingFraction, Date etc.) are important. For the evaluation one can change pcutoff. This cutoff also influences how likely estimated postions need to be so that they are shown in the plots. One can furthermore, change the colormap and dotsize for those graphs.

# In[5]:


deeplabcut.evaluate_network(path_config_file,plotting=False)


# *NOTE: depending on your set up sometimes you get some "matplotlib errors, but these are not important*
# 
# Now you can go check out the images. Given the limted data input and it took ~20 mins to test this out, it is not meant to track well, so don't be alarmed. This is just to get you familiar with the workflow... 

# ## Analyzing videos
# This function extracts the pose based on a trained network from videos. The user can choose the trained network - by default the most recent snapshot is used to analyse the videos. However, the user can also specify the snapshot index for the variable **snapshotindex** in the **config.yaml** file).
# 
# The results are stored in hd5 file in the same directory, where the video resides. The pose array (pose vs. frame index) can also be exported as csv file (set flag to...). 

# In[ ]:


# Creating video path:
import os
videofile_path = os.path.join(os.getcwd(),'openfield-Pranav-2018-10-30/videos/m3v1mp4.mp4')


# In[ ]:


print("Start analyzing the video!")
#our demo video on a CPU with take ~30 min to analze! GPU is much faster!
deeplabcut.analyze_videos(path_config_file,[videofile_path])


# ## Create labeled video
# 
# This function is for the visualization purpose and can be used to create a video in .mp4 format with the predicted labels. This video is saved in the same directory, where the (unlabeled) video resides. 
# 
# Various parameters can be set with regard to the colormap and the dotsize. The parameters of the 

# In[ ]:


deeplabcut.create_labeled_video(path_config_file,[videofile_path])


# ## Plot the trajectories of the analyzed videos
# This function plots the trajectories of all the body parts across the entire video. Each body part is identified by a unique color. The underlying functions can easily be customized.

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'notebook')
deeplabcut.plot_trajectories(path_config_file,[videofile_path],showfigures=True)

#These plots can are interactive and can be customized (see https://matplotlib.org/)


# ## Extract outlier frames, where the predictions are off.
# 
# This is optional step allows to add more training data when the evaluation results are poor. In such a case, the user can use the following function to extract frames where the labels are incorrectly predicted. Make sure to provide the correct value of the "iterations" as it will be used to create the unique directory where the extracted frames will be saved.

# In[ ]:


deeplabcut.extract_outlier_frames(path_config_file,[videofile_path])


# The user can run this iteratively, and (even) extract additional frames from the same video.

# ## Manually correct labels
# 
# This step allows the user to correct the labels in the extracted frames. Navigate to the folder corresponding to the video 'm3v1mp4' and use the GUI as described in the protocol to update the labels.

# In[ ]:


get_ipython().run_line_magic('gui', 'wx')
deeplabcut.refine_labels(path_config_file)


# In[ ]:


#Perhaps plot the labels to see how how all the frames are annoted (including the refined ones)
deeplabcut.check_labels(path_config_file)


# In[ ]:


# Now merge datasets (once you refined all frames)
deeplabcut.merge_datasets(path_config_file)


# ## Create a new iteration of training dataset, check it and train...
# 
# Following the refine labels, append these frames to the original dataset to create a new iteration of training dataset.

# In[ ]:


deeplabcut.create_training_dataset(path_config_file)


# Now one can train the network again... (with the expanded data set)

# In[ ]:


deeplabcut.train_network(path_config_file, shuffle=1)

