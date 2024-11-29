import winsound
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np
import matplotlib.pyplot as plt
import serial
# Setup Serial Communication
arduino_port = 'COM7' 
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
# Email Configuration
sender_email = "reportdefibrillator@gmail.com"
receiver_email = "alaa.tarek@eng.cu.edu.eg"
password = "xrrv xjhe ruun zade"

# SMTP Configuration
smtp_server = "smtp.gmail.com"  # e.g., smtp.gmail.com for Gmail
smtp_port = 587  # Standard SMTP port

def generate_realistic_pqrst_wave(sampling_rate=500):
    # Define timings and base amplitudes for the PQRST components
    p_duration = 0.08  # duration of P wave in seconds
    qrs_duration = 0.15  # duration of QRS complex in seconds
    t_duration = 0.1  # duration of T wave in seconds

    # Random variations for arrhythmia effect
    p_amp = 0.1 * np.random.uniform(0.9, 1.1)
    q_amp = -0.15 * np.random.uniform(0.9, 1.1)
    r_amp = 0.1 * np.random.uniform(0.9, 1.1)
    s_amp = -0.1 * np.random.uniform(0.9, 1.1)
    t_amp = 0.1 * np.random.uniform(0.9, 1.1)

    # Adjust timing offsets to add variability
    p_offset = 0.1 + np.random.uniform(-0.01, 0.01)
    q_offset = 0.2 + np.random.uniform(-0.01, 0.01)
    r_offset = 0.25 + np.random.uniform(-0.005, 0.005)
    s_offset = 0.3 + np.random.uniform(-0.005, 0.005)
    t_offset = 0.4 + np.random.uniform(-0.01, 0.01)

    # Create a time vector for one heartbeat
    beat_duration = 1  # 1 second for each beat
    t = np.linspace(0, beat_duration, int(sampling_rate * beat_duration), endpoint=False)

    # Generate each PQRST component with Gaussian-like shapes
    p_wave = p_amp * np.exp(-((t - p_offset) ** 2) / (2 * (p_duration / 4) ** 2))
    q_wave = q_amp * np.exp(-((t - q_offset) ** 2) / (2 * (qrs_duration / 10) ** 2))
    r_wave = r_amp * np.exp(-((t - r_offset) ** 2) / (2 * (qrs_duration / 20) ** 2))
    s_wave = s_amp * np.exp(-((t - s_offset) ** 2) / (2 * (qrs_duration / 10) ** 2))
    t_wave = t_amp * np.exp(-((t - t_offset) ** 2) / (2 * (t_duration / 4) ** 2))

    # Combine PQRST components to form a single ECG-like wave
    ecg_wave = p_wave + q_wave + r_wave + s_wave + t_wave
    return ecg_wave

def send_email(voltage , time):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Defibrillator Report"
    if(float(voltage) < 8.4 or float(time) > 160):
        body = f'''
    Defibrillator located at the hospital report on 7/11/2024:
    Battery Level charge: {voltage},
    Capacitor charging time: {time},
    Defibrillator has an error, please send a technician
    '''
    else:
        body = f'''
    Defibrillator located at the hospital report on 7/11/2024:
    Battery Level charge: {voltage},
    Capacitor charging time: {time},
    Defibrillator is working well
    '''
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Listen to Serial and trigger email
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        # line = "1"
        splitted_words = line.split("_")
        print(splitted_words)
        if(len(splitted_words)) == 2:
            print(f"Received: {splitted_words}")
            send_email(splitted_words[0] , splitted_words[1])
        elif(len(splitted_words) == 1):
            if(splitted_words[0] == '1'  ):
                sampling_rate = 500  
                num_beats = 10 

                
                ecg_signal = np.array([])
                time = np.array([])

                for beat in range(num_beats):
                    
                    pqrst_wave = generate_realistic_pqrst_wave(sampling_rate)

                    ecg_signal = np.concatenate((ecg_signal, pqrst_wave))

                    t = np.linspace(beat, beat + 1, len(pqrst_wave), endpoint=False)
                    time = np.concatenate((time, t))

                # Plot the simulated arrhythmic ECG
                winsound.Beep(1000 , 2000)
                plt.figure(figsize=(15, 5))
                plt.plot(time, ecg_signal)
                plt.title('Simulated Arrhythmic ECG-like Signal')
                plt.xlabel('Time (s)')
                plt.ylabel('Amplitude')
                plt.xlim(0, num_beats)  # Limit x-axis based on the total number of beats
                plt.show()
                
            else:
                print(f"Patient's Temperature: {splitted_words[0]}")

