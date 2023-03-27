import cv2
import numpy as np
import PoseEstimationModule as pem
import streamlit as st
import subprocess
import tempfile
import time
from Exercises import Curls, Pushups, Squats
from calories_burned import get_calories_burned
from duration import get_video_duration
from PIL import Image
from report import report_sender



st.title('AI Fitness Trainer')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('AI Fitness Trainer')



# @st.cache_resource()


def render_curls_trainer(video_file_buffer):
    DEMO_VIDEO = "TrainerVideos/curls_aminu.mp4"
    if not video_file_buffer:
        if use_webcam:
            capturedVideo = cv2.VideoCapture(1)
        else:
            capturedVideo = cv2.VideoCapture(DEMO_VIDEO)
            tmpfile.name = DEMO_VIDEO
    
    else:
        tmpfile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tmpfile.name)

    width = int(capturedVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capturedVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    input_fps = int(capturedVideo.get(cv2.CAP_PROP_FPS))

    
    out = cv2.VideoWriter('curls_recording.avi', 
                         cv2.VideoWriter_fourcc('M','J','P','G'),
                         input_fps, (1280,720))
   
    st.sidebar.text('Input Video')
    st.sidebar.video(tmpfile.name)

    fps = 0
    i = 0

    kpi1, kpi2 = st.columns(2)

    with kpi1:
        st.markdown("**FrameRate**")
        kpi1_text = st.markdown("0")

    with kpi2:
        st.markdown("**Image Width**")
        kpi2_text = st.markdown("0")
    
    st.markdown("<hr/>", unsafe_allow_html=True)

     
    pose_detector = pem.PoseDetector(min_detection_confidence=detection_confidence,
          min_tracking_confidence=tracking_confidence)

    count = 0
    previous_time = 0
    direction = "upwards" #assigns direction of curl as upward

    while capturedVideo.isOpened():
        success, img = capturedVideo.read()
        if not success: #break if video or image has ended
            break #break?

        img = cv2.resize(img, (1280, 720)) #resize video
        img = pose_detector.find_pose(img, False)  #find pose but do not draw so as to focus on the three points angle is going to be calculated for.
        landmarks = pose_detector.find_landmarks(img, False) #find landmarks 
        # print(landmarks)

        
        if len(landmarks) != 0: #check that landmarks were found
            
            exercise = Curls.Curls(pose_detector, img, count, direction)            
            count, direction = exercise.get_curls_count()

        
            print(count)
        
        
            # Draw Bar
            cv2.rectangle(img, (1100,100), (1175,650), exercise.color, 4) #draws unfilled rectangle that dynamic bar is going to be placed in.
            cv2.rectangle(img, (1100,int(exercise.bar)), (1175,650),exercise.color, cv2.FILLED) #draws rectangle whose size changes depending on the bar value.
            cv2.putText(img, str(int(exercise.percent)) + "%", (1100, 75),
                        cv2.FONT_HERSHEY_PLAIN, 4, exercise.color,4)    #renders the text string (i.e.percent) in img.
                

            # Draw Curl Count
            cv2.rectangle(img, (0,500), (200,720), (0,255, 0), cv2.FILLED) #draws a filled rectangle (bar) that the exercise count is going to be placed in.
            cv2.putText(img, str(int(count)), (25, 700),
                        cv2.FONT_HERSHEY_PLAIN, 15, (255,255,255),25)    #renders the text string (i.e.count) in img.
                
            current_time = time.time()
            fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
            previous_time = current_time
            cv2.putText(img, "fps= " + str(int(fps)), (50, 100),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),5)    #renders the text string (i.e.fps) in img.

        
            if record:
                #st.checkbox("Recording", value=True)
                out.write(img)
            #Dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{width}</h1>", unsafe_allow_html=True)

            img = cv2.resize(img,(0,0),fx = 0.8 , fy = 0.8)
            img = image_resize(image = img, width = 640)
            stframe.image(img,channels = 'BGR',use_column_width=True)


    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

    st.text('Recorded Video')

    input_file = 'curls_recording.avi'
    output_file = 'curls_recording.mp4'

    # FFmpeg command to convert AVI to MP4
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', "-y", output_file]

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_cmd)

    st.video('curls_recording.mp4')

    capturedVideo.release()
    out.release()

    return count


def render_pushups_trainer(video_file_buffer):
    DEMO_VIDEO = "TrainerVideos/pushups_aminu.mp4"
    if not video_file_buffer:
        if use_webcam:
            capturedVideo = cv2.VideoCapture(1)
        else:
            capturedVideo = cv2.VideoCapture(DEMO_VIDEO)
            tmpfile.name = DEMO_VIDEO
    
    else:
        tmpfile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tmpfile.name)

    width = int(capturedVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capturedVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    input_fps = int(capturedVideo.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter('pushups_recording.avi', 
                         cv2.VideoWriter_fourcc('M','J','P','G'),
                         input_fps, (1280,720))

    st.sidebar.text('Input Video')
    st.sidebar.video(tmpfile.name)

    fps = 0
    i = 0

    kpi1, kpi2 = st.columns(2)

    with kpi1:
        st.markdown("**FrameRate**")
        kpi1_text = st.markdown("0")

    with kpi2:
        st.markdown("**Image Width**")
        kpi2_text = st.markdown("0")
    
    st.markdown("<hr/>", unsafe_allow_html=True)

     
    pose_detector = pem.PoseDetector(min_detection_confidence=detection_confidence,
          min_tracking_confidence=tracking_confidence)

    count = 0
    previous_time = 0
    direction = "upwards" #assigns direction of pushup as upward

    while capturedVideo.isOpened():
        success, img = capturedVideo.read()
        if not success: #break if video or image has ended
            break #continue?

        img = cv2.resize(img, (1280, 720)) #resize video
        img = pose_detector.find_pose(img, False)  #find pose but do not draw so as to focus on the three points angle is going to be calculated for.
        landmarks = pose_detector.find_landmarks(img, False) #find landmarks 
        # print(landmarks)

        
        if len(landmarks) != 0: #check that landmarks were found
            
            exercise = Pushups.Pushups(pose_detector, img, count, direction)            
            count, direction = exercise.get_pushups_count()

        
            print(count)
        
        
            # Draw Bar
            cv2.rectangle(img, (1100,100), (1175,650), exercise.color, 4) #draws unfilled rectangle that dynamic bar is going to be placed in.
            cv2.rectangle(img, (1100,int(exercise.bar)), (1175,650),exercise.color, cv2.FILLED) #draws rectangle whose size changes depending on the bar value.
            cv2.putText(img, str(int(exercise.percent)) + "%", (1100, 75),
                        cv2.FONT_HERSHEY_PLAIN, 4, exercise.color,4)    #renders the text string (i.e.percent) in img.
                

            # Draw Pushup Count
            cv2.rectangle(img, (0,500), (200,720), (0,255, 0), cv2.FILLED) #draws a filled rectangle (bar) that the exercise count is going to be placed in.
            cv2.putText(img, str(int(count)), (25, 700),
                        cv2.FONT_HERSHEY_PLAIN, 15, (255,255,255),25)    #renders the text string (i.e.count) in img.
                
            current_time = time.time()
            fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
            previous_time = current_time
            cv2.putText(img, "fps= " + str(int(fps)), (50, 100),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),5)    #renders the text string (i.e.fps) in img.

        
            if record:
                #st.checkbox("Recording", value=True)
                out.write(img)
            #Dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{width}</h1>", unsafe_allow_html=True)

            img = cv2.resize(img,(0,0),fx = 0.8 , fy = 0.8)
            img = image_resize(image = img, width = 640)
            stframe.image(img,channels = 'BGR',use_column_width=True)


    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

    st.text('Recorded Video')

    # recorded_video = open('pushups_recording.avi','rb')
    # # recorded_video = open('TrainerVideos/pushups.mp4','rb')
    # out_bytes = recorded_video.read()
    # st.video(out_bytes)


    input_file = 'pushups_recording.avi'
    output_file = 'pushups_recording.mp4'

    # FFmpeg command to convert AVI to MP4
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', "-y", output_file]

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_cmd)

    st.video('pushups_recording.mp4')


    capturedVideo.release()
    out.release()
    
    return count

def render_squats_trainer(video_file_buffer):
    DEMO_VIDEO = "TrainerVideos/squats_aminu.mp4"
    if not video_file_buffer:
        if use_webcam:
            capturedVideo = cv2.VideoCapture(1)
        else:
            capturedVideo = cv2.VideoCapture(DEMO_VIDEO)
            tmpfile.name = DEMO_VIDEO
    
    else:
        tmpfile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tmpfile.name)

    width = int(capturedVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capturedVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    input_fps = int(capturedVideo.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter('squats_recording.avi', 
                         cv2.VideoWriter_fourcc('M','J','P','G'),
                         input_fps, (1280,720))

    st.sidebar.text('Input Video')
    st.sidebar.video(tmpfile.name)

    fps = 0
    i = 0

    kpi1, kpi2 = st.columns(2)

    with kpi1:
        st.markdown("**FrameRate**")
        kpi1_text = st.markdown("0")

    with kpi2:
        st.markdown("**Image Width**")
        kpi2_text = st.markdown("0")
    
    st.markdown("<hr/>", unsafe_allow_html=True)

     
    pose_detector = pem.PoseDetector(min_detection_confidence=detection_confidence,
          min_tracking_confidence=tracking_confidence)

    count = 0
    previous_time = 0
    direction = "upwards" #assigns direction of squats as upward

    while capturedVideo.isOpened():
        success, img = capturedVideo.read()
        if not success: #break if video or image has ended
            break #continue?

        img = cv2.resize(img, (1280, 720)) #resize video
        img = pose_detector.find_pose(img, False)  #find pose but do not draw so as to focus on the three points angle is going to be calculated for.
        landmarks = pose_detector.find_landmarks(img, False) #find landmarks 
        # print(landmarks)

        
        if len(landmarks) != 0: #check that landmarks were found
            
            exercise = Squats.Squats(pose_detector, img, count, direction)            
            count, direction = exercise.get_squats_count()

        
            print(count)
        
        
            # Draw Bar
            cv2.rectangle(img, (1100,100), (1175,650), exercise.color, 4) #draws unfilled rectangle that dynamic bar is going to be placed in.
            cv2.rectangle(img, (1100,int(exercise.bar)), (1175,650),exercise.color, cv2.FILLED) #draws rectangle whose size changes depending on the bar value.
            cv2.putText(img, str(int(exercise.percent)) + "%", (1100, 75),
                        cv2.FONT_HERSHEY_PLAIN, 4, exercise.color,4)    #renders the text string (i.e.percent) in img.
                

            # Draw Squat Count
            cv2.rectangle(img, (0,500), (200,720), (0,255, 0), cv2.FILLED) #draws a filled rectangle (bar) that the exercise count is going to be placed in.
            cv2.putText(img, str(int(count)), (25, 700),
                        cv2.FONT_HERSHEY_PLAIN, 15, (255,255,255),25)    #renders the text string (i.e.count) in img.
                
            current_time = time.time()
            fps = 1/(current_time - previous_time)  #calculates frame per second i.e. frame rate.
            previous_time = current_time
            cv2.putText(img, "fps= " + str(int(fps)), (50, 100),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),5)    #renders the text string (i.e.fps) in img.

        
            if record:
                #st.checkbox("Recording", value=True)
                out.write(img)
            #Dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{width}</h1>", unsafe_allow_html=True)

            img = cv2.resize(img,(0,0),fx = 0.8 , fy = 0.8)
            img = image_resize(image = img, width = 640)
            stframe.image(img,channels = 'BGR',use_column_width=True)


    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

    st.text('Recorded Video')

    input_file = 'squats_recording.avi'
    output_file = 'squats_recording.mp4'

    # FFmpeg command to convert AVI to MP4
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac', '-b:a', '128k', "-y", output_file]

    # Execute the FFmpeg command
    subprocess.run(ffmpeg_cmd)

    st.video('squats_recording.mp4')

    capturedVideo.release()
    out.release()

    return count



@st.cache_resource()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

# @st.cache_resource()
def render_body_weight():
    body_weight = st.text_input("Enter your weight in Kg")
    return body_weight

# @st.cache_resource()
def render_email_address():
    email_address = st.text_input("Enter your email address")
    return email_address

st.cache_resource()
def render_weight_and_email():
    input_text = st.text_input("Enter weight (Kg) and email address in format weight email e.g. 60 myemail@domain.com")
    weight_and_email = input_text.split()
    return weight_and_email


about = st.sidebar.button("About App")


if about:
    about_project = '''
    **TL; DR:** The goal of the project can be summarized as developing an AI fitness trainer embedded with storage and recommender systems and an AI virtual mouse.

    ## Goals
    - Help the user lose weight, gain muscle, and accomplish other fitness goals.
    - Attempt to understand the user goals and develop a fitness routine.
    - Recommend a healthy eating plan.
    - Ensure all exercises are performed correctly.

    ## Motivation

    - To enhance exposure in the exciting computer vision (CV) field. 
    - Drive to apply CV in automating “everyday” activities like the process of getting fit. 
        - For instance, taking on activities like bouldering and hiking to stay fit have not given me desired results. 
        - If I had an AI Fitness Trainer, accomplishing my fitness goals would have been much easier. 

    ## Impact

    - The project is a win-win for both the developer and the users.
        - the developer gets to enhance their experience while working on something they are super interested in, and 
        - the users get a fantastic product that satisfies their need. 
        

    ## Technical Details and Stack

    Overall, the architecture is built on a combination of computer vision, natural language processing, machine learning, and storage and recommender systems to 
    provide a comprehensive and personalized fitness training experience.

    - **Web App Dev:** Streamlit framework was used to develop the User Interface (UI), which includes features like displaying workout routines.
    - **Computer Vision:** Utilized OpenCV for capturing and processing images/videos, and the Mediapipe BlazePose model to detect 33 posture landmarks in real-time. These landmarks are used to calculate angles between different parts of the body during exercises.
    - **Machine Learning:** Incorporated machine learning algorithms to analyze user data and provide personalized recommendations for workouts and healthy eating plans. 
    - **Natural Language Processing (NLP):** Employed the Google Text-to-Speech (gTTS) API and speech_recognition library to convert text to speech and recognize user commands. 
    - **Storage and Recommender System:** Leveraged the smtplib, MIMEMultipart, and MIMEText modules to implement a report-sending feature. Used SQLite to store user information and workout history, and use data analysis and machine learning algorithms to generate personalized workout plans and healthy eating recommendations based on user data and preferences.
    - **Audio:** Utilized the playsound module to play audio, which could be used to provide audio feedback or instructions during exercises.

            
    Here is the link to the project repo: [AI Fitness Trainer Github Repo](https://www.github.com/in/aminuabdusalam/AI-FitnessTrainer)
    '''
    st.markdown(about_project)

    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    about_me = '''
    # About Me 
    Hola! I'm Aminu Abdusalam - the one and only so any other one is *counterfeit*. Just kidding haha!

    ## Education

    - Bachelor's degree in Computer Science from Fisk University (currently enrolled)


    ## Experience

    - Program Management Intern at Microsoft Corp (2022)
    - Program Management and Software Engineering Intern at Microsoft (2021)
    - Information Technology Intern at Froedtert Health (2020)

    ## Skills

    - Python
    - Java
    - HTML/CSS
    - Kusto/SQL

    Connect with me at [LinkedIn](https://www.linkedin.com/in/aminuabdusalam)

    And check out my other works at [Github](https://www.github.com/in/aminuabdusalam)
                
    '''
    st.markdown(about_me)


    
st.sidebar.subheader('Parameters')
app_mode = st.sidebar.selectbox('Select Exercise Choice',
['Curls','Squats', 'Pushups', 'GenerateReport']
)


# Create global variables using st.session_state
if "exercise_type" not in st.session_state:
    st.session_state.exercise_type = None 
if "report_count" not in st.session_state:
    st.session_state.report_count = 0



if (app_mode == "Curls" or app_mode == "Pushups" or app_mode == "Squats") and not about:

    st.set_option('deprecation.showfileUploaderEncoding', False)

    use_webcam = st.sidebar.button('Use Webcam')
    record = st.sidebar.checkbox("Record Video")
    if record:
        st.checkbox("Recording", value=True)

    st.sidebar.markdown('---')
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
        )

    detection_confidence = st.sidebar.slider('Minimum Detection Confidence', min_value =0.0,max_value = 1.0,value = 0.5)
    tracking_confidence = st.sidebar.slider('Minimum Tracking Confidence', min_value = 0.0,max_value = 1.0,value = 0.5) #for the pose landmarks to be considered tracked successfully, or otherwise person detection will be invoked automatically on the next input image.

    st.sidebar.markdown('---')

    st.markdown(' ## Output')

    stframe = st.empty()
    video_file_buffer = st.sidebar.file_uploader("Upload a video", type=[ "mp4", "mov",'avi','asf', 'm4v' ])
    tmpfile = tempfile.NamedTemporaryFile(delete=False)


    if app_mode == "Curls" and not about and app_mode != "GenerateReport":
        
        st.session_state.report_count = render_curls_trainer(video_file_buffer)
        st.session_state.exercise_type= "curls"
        st.write("latest exercise type: " + str(st.session_state.exercise_type))
        st.write(st.session_state.exercise_type + " count: " + str(st.session_state.report_count))
        # st.markdown("[Generate Report](?page=GenerateReport)")

    if app_mode == "Pushups" and not about and app_mode != "GenerateReport":
        st.session_state.report_count = render_pushups_trainer(video_file_buffer)
        st.session_state.exercise_type= "pushups"
        st.write("latest exercise type: " + str(st.session_state.exercise_type))
        st.write(st.session_state.exercise_type + " count: " + str(st.session_state.report_count))


    if app_mode == "Squats" and not about and app_mode != "GenerateReport":
        st.session_state.report_count = render_squats_trainer(video_file_buffer)
        st.session_state.exercise_type= "squats"
        st.write("latest exercise type: " + str(st.session_state.exercise_type))
        st.write(st.session_state.exercise_type + " count: " + str(st.session_state.report_count))

    
if app_mode == "GenerateReport" and app_mode != "Curls" and app_mode != "Pushups" and app_mode != "Squats" and not about:
    st.write("latest exercise type: " + str(st.session_state.exercise_type))
    st.write(st.session_state.exercise_type + " count: " + str(st.session_state.report_count))
    with st.form("my_form"):
            input_text = st.text_input("Enter weight (Kg) and email address in format weight email e.g. 60 myemail@domain.com")
            submit_button = st.form_submit_button(label="Submit")
            input_texted = input_text.split()    
            if input_texted:
                body_weight, email_address = input_texted[0], input_texted[1]
                calories_burned, duration = get_calories_burned(st.session_state.exercise_type, body_weight, st.session_state.report_count)
    # Call the function only if the submit button is clicked
    if submit_button:
        report_sender(email_address, duration, calories_burned)


    # Create a form that contains a text box and a submit button

    # Create an input text box
    # body_weight = st.text_input("Enter your body_weight in Kg here")
    # # Initialize the session state variable
    # if "my_input_value1" not in st.session_state:
    #     st.session_state.my_input_value1 = """


    # body_weight = st.session_state.my_input_value1
    # # body_weight = ""
    # if not body_weight:
    #     body_weight = render_body_weight()
    #     #store the updated value in the session state
    #     st.session_state.my_input_value1 = body_weight
    #     st.write("Body weight:", body_weight)

    # email_address = st.session_state.my_input_value2
    # # email_address = ""
    # if not email_address:
    #     email_address = render_email_address()
    #     st.session_state.my_input_value2 = email_address
    #     st.write("Email address:", email_address)


    # if body_weight and email_address:
    #     send_report = st.button("Send Report")
    #     calories_burned, duration = get_calories_burned('curls', body_weight, count)
    #     if send_report:
    #         report_sender(email_address, duration, calories_burned)
        




# with st.form("my_form"):
#     input_text = st.text_input("Enter some text:")
#     submit_button = st.form_submit_button(label="Submit")
#     input_texted = input_text.split()    
#     body_weight, email_address = input_texted[0], input_texted[1]
#     calories_burned, duration = get_calories_burned('curls', body_weight, count)
# # Call the function only if the submit button is clicked
# if submit_button:
#     report_sender(email_address, duration, calories_burned)


