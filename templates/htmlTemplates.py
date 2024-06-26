css = '''
<style>
/* Base styles for chat messages */
.chat-message {
    border-radius: 8px;
    margin-bottom: 16px;
    display: flex;
    justify-content: flex-start; /* Align content to the left */
    align-items: center; /* Center vertically */
}

.chat-message.user {
    background-color: #2f1604;
}

.chat-message.bot {
    background-color: rgb(108 109 133 / 50%);
}

.chat-message .avatar {
    width: 20%;
    margin-right: 2px;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    object-fit: cover;
}

.chat-message.user .avatar img {
    border-radius: 80%; /* User avatar border-radius */
}

.chat-message.bot .avatar img {
    border-radius: 80px;
}

.chat-message .message {
    width: 80%;
    padding: 4px 8px; /* Adjust padding as needed */
    color: #fff;
}

/* Media query for responsive design */
@media screen and (max-width: 768px) {
    .chat-message {
        flex-direction: column; /* Stack elements vertically */
        align-items: flex-start; /* Align elements to the left */
    }

    .chat-message .avatar {
        width: 100%; /* Avatar takes full width on small screens */
        margin-bottom: 8px; /* Add spacing between avatar and message */
    }
}

</style>


'''
# <a href="https://imgbb.com/"><img src="https://i.ibb.co/nnQZRNp/mydp.png" alt="mydp" border="0"></a>
# https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png

# <a href="https://ibb.co/ZzDhZMW"><img src="https://i.ibb.co/1GW9Sm8/user.jpg" alt="user" border="0"></a>
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/1GW9Sm8/user.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
# https://i.ibb.co/rdZC7LZ/Photo-logo-1.png
