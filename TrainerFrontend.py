import cv2
import numpy as np
import PoseEstimationModule as pem
import streamlit as st
import tempfile
import time
from Exercises import Curls, Pushups, Squats
from PIL import Image


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
st.sidebar.subheader('Parameters')


@st.cache()
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

app_mode = st.sidebar.selectbox('Choose the Exercise',
['About App','Curls','Squats', 'Pushups']
)

if app_mode == "Curls":
    DEMO_VIDEO = "TrainerVideos/curls.mp4"

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

    if not video_file_buffer:
        if use_webcam:
            capturedVideo = cv2.VideoCapture(0)
        else:
            capturedVideo = cv2.VideoCapture(DEMO_VIDEO)
            tmpfile.name = DEMO_VIDEO
    
    else:
        tmpfile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tmpfile.name)

    width = int(capturedVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capturedVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    input_fps = int(capturedVideo.get(cv2.CAP_PROP_FPS))

    codec = cv2.VideoWriter_fourcc('V','P','0','9')
    out = cv2.VideoWriter('output1.mp4', codec, input_fps, (width, height))

    st.sidebar.text('Input Video')
    st.sidebar.video(tmpfile.name)

    fps = 0
    i = 0

    kpi1, kpi2 = st.beta_columns(2)

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
            break #continue?

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

    st.text('Video Processed')

    output_video = open('output1.mp4','rb')
    out_bytes = output_video.read()
    st.video(out_bytes)

    capturedVideo.release()
    out.release()


