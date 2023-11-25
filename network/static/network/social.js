// --- MAIN --- //

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    //document.querySelector('#feed').addEventListener('click', () => load_posts(user));
    document.querySelector('#new_post_button').addEventListener('click', compose_new_post);
    document.querySelector('#edit_profile_button').addEventListener('click', edit_profile);
    document.querySelector('#following_button').addEventListener('click', switch_following_view);
    document.querySelector('#followers_button').addEventListener('click', switch_follower_view);
    document.querySelector('#compose_comment_form').addEventListener('submit', postComment);
    //document.querySelectorAll('#edit_post_button').forEach(addEventListener('click', editOwnPost));

    // By default, load the feed
    load_posts();
  });


// --- LOADING POSTS --- //

function load_posts() {
    // Show the feed, profile & followers and hide other views
    document.querySelector('#feed').style.display = 'flex';
    document.querySelector('#own_profile').style.display = 'flex';
    document.querySelector('#followers').style.display = 'flex';
    document.querySelector('#following').style.display = 'none';
    document.querySelector('#new_post').style.display = 'none';
    document.querySelector('#edit_profile').style.display = 'none';
    document.querySelector('#view_profile').style.display = 'none';
    document.querySelector('#comment_view').style.display = 'none';
    document.querySelector('#edit_post_view').style.display = 'none';

}

// --- NEW POST --- //

function compose_new_post() {
  event.preventDefault();
  // Show compose view and hide other views
  document.querySelector('#feed').style.display = 'block';
  document.querySelector('#own_profile').style.display = 'none';
  document.querySelector('#followers').style.display = 'block';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#new_post').style.display = 'flex';
  document.querySelector('#edit_profile').style.display = 'none';
  document.querySelector('#view_profile').style.display = 'none';
  document.querySelector('#comment_view').style.display = 'none';
  document.querySelector('#edit_post_view').style.display = 'none';
}


// --- EDIT PROFILE--- //

function edit_profile() {
  event.preventDefault();
  // Show edit profile view and hide other views
  document.querySelector('#feed').style.display = 'block';
  document.querySelector('#own_profile').style.display = 'none';
  document.querySelector('#followers').style.display = 'block';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#new_post').style.display = 'none';
  document.querySelector('#edit_profile').style.display = 'flex';
  document.querySelector('#view_profile').style.display = 'none';
  document.querySelector('#comment_view').style.display = 'none';
  document.querySelector('#edit_post_view').style.display = 'none';
}



// --- VIEW POST --- //

function viewProfile(other_user_id) {
  event.preventDefault();
  // Show view profile view and hide other views
  document.querySelector('#feed').style.display = 'block';
  document.querySelector('#own_profile').style.display = 'none';
  document.querySelector('#followers').style.display = 'block';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#new_post').style.display = 'none';
  document.querySelector('#edit_profile').style.display = 'none';
  document.querySelector('#view_profile').style.display = 'block';
  document.querySelector('#comment_view').style.display = 'none';
  document.querySelector('#edit_post_view').style.display = 'none';

  //getting user
  fetch(`/view_profile/${other_user_id}`)
  .then(response => response.json())
  .then(profile => {
    // Print profile
    console.log(profile);
    //display the profile info in a div
    var currentUserId = document.getElementById("current_user_id_from_input").value;
    document.querySelector('#other_user_profile_div').innerHTML =
    `
    <div style="display: flex; flex-direction:row; justify-content: space-between; padding:0;">
      <h6 style="text-align: left; margin-left: 10px;">@${profile.username}</h6>
      <a class="round" onclick="followUser(${profile.id},${currentUserId}); getFollowed(${profile.id},${currentUserId})" style="padding-top: 2px; padding-left:0.5px; margin-right: 10px; margin-top: 5px;" title="Follow user" id="follow_button">
        <i class="fa-solid fa-user-plus"></i>
      </a>
    </div>
    <img src="${profile.profile_photo}" alt="Profile photo" width=100%>
    <div style="display: flex; flex-direction:column; justify-content: center; align-items: start;">
        <br>
        <h6>First name: ${profile.first_name}</h6>
        <h6>Last name: ${profile.last_name}</h6>
        <h6>E-mail: ${profile.email}</h6>
        <h6>Bio:</h6>
        <p style="margin:10px; text-align:left;">${profile.bio}</p>
        <br>
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; width: 100%; margin: auto; margin-top:-10px;">
            <div>
                <h6 style="text-align:center; margin-bottom:0px; font-size: 12px;"> ${profile.posts.length}</h6>
                <p>posts</p>
            </div>
            <div>
                <h6 style="text-align:center; margin-bottom:0px; font-size: 12px;">${profile.followers.length}</h6>
                <p>followers</p>
            </div>
            <div>
                <h6 style="text-align:center; margin-bottom:0px; font-size: 12px;">${profile.following.length}</h6>
                <p>following</p>
            </div>
        </div>
        <br>
    </div>
    `;
    //show user's posts
    fetch(`/posts/${other_user_id}`)
    .then(response => response.json())
    .then(posts => {
      var currentUserId = document.getElementById("current_user_id_from_input").value;
      posts.forEach(post => {
        let newDiv = document.createElement('div');
        newDiv.innerHTML =
        `
        <div class="popup-rectangle">
              <div class="post">
                  <a class="link">
                      @${profile.username}
                  </a>
                  <img src="${post.photo}" alt="Post photo" width=100%>
                  <div style="display: flex; flex-direction: row;">
                      <h6 style="text-align:left; margin-top: 15px;">${post.date}</h6>
                      <div style="display:flex; flex-direction:row; justify-content: center; align-items: center; margin-top: 10px; margin-left:auto; margin-right: 10px;">
                          <p class="likes_number" id="likes_number">${post.liked_by.length} likes</p>
                          <button class="round" onclick="likeUnlike(${post.id},${currentUserId})" title="Like post">
                              <i class="fa-solid fa-heart"></i>
                          </button>
                          <button class="round" onclick="followUser(${profile.id}, ${currentUserId}); getFollowed(${profile.id},${currentUserId})" style="display: block;" title="Follow user" id="follow_button">
                              <i class="fa-solid fa-user-plus"></i>
                          </button>
                          <button class="round" id="comment_button" onclick="commentView(${post.id})" title="Comments view">
                              <i class="fa-solid fa-comment"></i>
                          </button>
                      </div>
                  </div>
                  <p class="post-description">${post.description}</p>
              </div>
          </div>
          `;
          document.getElementById("other_user_posts").appendChild(newDiv);
        });
      });
      });

}





// --- FOLLOWERS --- //

function switch_following_view() {
  event.preventDefault();
  // Show edit profile view and hide other views
  document.querySelector('#feed').style.display = 'block';
  document.querySelector('#own_profile').style.display = 'block';
  document.querySelector('#followers').style.display = 'none';
  document.querySelector('#following').style.display = 'block';
  document.querySelector('#new_post').style.display = 'none';
  document.querySelector('#edit_profile').style.display = 'none';
  document.querySelector('#view_profile').style.display = 'none';
  document.querySelector('#comment_view').style.display = 'none';
  document.querySelector('#edit_post_view').style.display = 'none';
}




function switch_follower_view() {
  event.preventDefault();
  // Show edit profile view and hide other views
  document.querySelector('#feed').style.display = 'block';
  document.querySelector('#own_profile').style.display = 'block';
  document.querySelector('#followers').style.display = 'flex';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#new_post').style.display = 'none';
  document.querySelector('#edit_profile').style.display = 'none';
  document.querySelector('#view_profile').style.display = 'none';
  document.querySelector('#comment_view').style.display = 'none';
  document.querySelector('#edit_post_view').style.display = 'none';
}





// --- COMMENTS --- //

function commentView(post_id) {
  event.preventDefault();
  // Show edit profile view and hide other views
  document.querySelector('#feed').style.display = 'none';
  document.querySelector('#own_profile').style.display = 'block';
  document.querySelector('#followers').style.display = 'flex';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#new_post').style.display = 'none';
  document.querySelector('#edit_profile').style.display = 'none';
  document.querySelector('#view_profile').style.display = 'none';
  document.querySelector('#comment_view').style.display = 'flex';
  document.querySelector('#edit_post_view').style.display = 'none';

  //csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  //getting the post detail view
  fetch(`/post_view/${post_id}`)
  .then(response => response.json())
  .then(post => {
    // Print profile
    console.log(post);
    //display the profile info in a div
    document.querySelector('#post_comment_view_div').innerHTML =
    `
    <h6 style="text-align: left;">
      <a href="#" onclick="view_profile(${post.user.id})" style="color:white;" id="view_profile_button2">
          @${post.user}
      </a>
    </h6>

    <img src="${post.photo}" alt="Post photo" width=100%>
    <div style="display: flex; flex-direction: row;">
        <h6 style="text-align:left; margin-top: 15px;">${post.date}</h6>
        <div style="display:flex; flex-direction:row; margin-top: 10px; margin-left:auto; margin-right:10px;">
            <a class="round" href="#" style="display: block; margin-right:10px;" title="Follow user" id="follow_button">
                <i class="fa-solid fa-user-plus"></i>
            </a>
            <button class="round">
                <i class="fa-solid fa-heart"></i>
            </button>
        </div>
    </div>
    <p class="post-description">${post.description}</p>
    <input type="hidden" value="${post.id}" id="current_post_id">
    <br>
    `;

    //Add comments section
    let comments = post.comments
    console.log(comments);

    if (comments.length === 0){
      document.querySelector('#comments_list').innerHTML =
      `
      <p>There are no comments yet.</p>
      `
    } else {
          comments.forEach(comment => {
            fetch(`view_comment/${comment}`)
            .then (response => response.json())
            .then(comment => {
              // Print profile
              console.log(comment);
              const singleComment = document.createElement('div');
              singleComment.innerHTML =
              `
              <div style="display:flex; flex-direction:row; margin-top: 10px; padding:20px; background: rgba(255,255,255,0.2);">
                <img src="${comment.user_photo}" alt="avatar" width="35" height="35" style="object-fit: cover;">
                <div style="margin-left: 5px;">
                  <p style="font-size: 11px; margin-bottom: 2px;">${comment.user}</p>
                  <p style="margin-left:0px;">${comment.text}</p>
                </div>
              </div>
                `;
                document.querySelector('#comments_list').append(singleComment);
            })
            });
          };
      });
}





function postComment(event) {
  event.preventDefault();
  //csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');


  //get the comment info
  const text    = document.querySelector('#comment_text').value;
  const post_id = document.getElementById("current_post_id").value;
  console.log(text);

  fetch(`/comment`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": csrftoken,
      "Accept": "application/json",
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: text,
      post_id: post_id})
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      //commentView(post_id);
    });
}






// --- LIKE / UNLIKE --- //

function likeUnlike(post_id, currentUserId) {
  event.preventDefault();

  //csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  //getting the post detail view
  fetch(`/like_unlike/${post_id}/${currentUserId}`)
  .then(response => response.json())
  .then(post => {
    const liked_by_list = post.liked_by;
    var userId = currentUserId
    //when button clicked check if this person liked the post
    if (liked_by_list.includes(userId)) {
      indexUserId = liked_by_list.indexOf(userId);
      liked_by_list.splice(indexUserId, 1)
    } else {
      liked_by_list.push(userId)
    };
    //saving new no. of likes
    fetch(`/like_unlike/${post_id}/${currentUserId}`, {
      method: 'PUT',
      credentials: 'same-origin',
      headers: {
        "X-CSRFToken": csrftoken,
        "Accept": "application/json",
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        liked_by: liked_by_list})
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(liked_by_list);
      });
      //update likes number
      document.getElementById('likes_number').innerHTML = liked_by_list.length + " likes"
  });

}


// --- FOLLOW USER --- //
function followUser(another_user_id, currentUserId) {
  event.preventDefault();
  //csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }}}
    return cookieValue;
  }

  const csrftoken = getCookie('csrftoken');

  //getting logged-in user following list
  fetch(`/follow_user/${currentUserId}/${another_user_id}`)
  .then(response => response.json())
  .then(profile3 => {
    let following = profile3.following;
    if (following.includes(another_user_id)) {
      const index = following.indexOf(another_user_id);
      following.splice(index, 1);
      var newFollowing = following;
    }else{
      following.push(another_user_id);
      var newFollowing = following;
    };
    console.log(newFollowing);
    //getting other_user_id into current user following list
    fetch(`/follow_user/${currentUserId}/${another_user_id}`, {
      method: 'PUT',
      credentials: 'same-origin',
      headers: {
        "X-CSRFToken": csrftoken,
        "Accept": "application/json",
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        following: newFollowing
      }),
    });
    // Print result
    console.log(`Following: ${newFollowing}`);
    const followingAmount = newFollowing.length;
    //update likes number
    document.getElementById('user_number_following').innerHTML = followingAmount
    });

}



// --- GET FOLLOWED --- //
function getFollowed(another_user_id, currentUserId) {
  event.preventDefault();
  //csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }}}
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  //getting other user's followers list
  fetch(`/get_followed/${another_user_id}/${currentUserId}`)
  .then(response => response.json())
  .then(profile2 => {
    let followers = profile2.followers;
    //getting current user id
    if (followers.includes(currentUserId)) {
      const index = followers.indexOf(currentUserId);
      followers.splice(index, 1);
      var newFollowers = followers;
    }else{
      followers.push(currentUserId);
      var newFollowers = followers;
    };
    //getting current user id into another user followers list
    fetch(`/get_followed/${another_user_id}/${currentUserId}`, {
      method: 'PUT',
      credentials: 'same-origin',
      headers: {
        "X-CSRFToken": csrftoken,
        "Accept": "application/json",
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        followers: newFollowers
      })
    })

    // Print result
    console.log(`Followers: ${newFollowers}`);

  });

}


//--- EDIT OWN POST ---//
function editOwnPost(post_id) {
  event.preventDefault();
  // Show the feed, profile & followers and hide other views
  document.querySelector('#feed').style.display = 'block';
  document.querySelector('#own_profile').style.display = 'none';
  document.querySelector('#followers').style.display = 'flex';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#new_post').style.display = 'none';
  document.querySelector('#edit_profile').style.display = 'none';
  document.querySelector('#view_profile').style.display = 'none';
  document.querySelector('#comment_view').style.display = 'none';
  document.querySelector('#edit_post_view').style.display = 'block';

  //csrf
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }}}
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  //getting the post detail view
  fetch(`/edit_post/${post_id}`)
  .then(response => response.json())
  .then(post => {
    // Print profile
    console.log(post);
    document.getElementById("edit_current_photo").innerHTML =
    `
    <img src="${post.photo}" alt="Post photo" width=100%>
    `;
    document.getElementById("compose_post_form").insertAdjacentHTML('afterbegin',
    `
    <form action="edit_post/${post.id}" method="POST"  id="compose_post_form" enctype='multipart/form-data' style="display: flex; flex-direction:column; justify-content: center; align-items: start;">
    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
      <textarea class="post_description" rows="5" id="new_post_description_textarea" name="new_post_description_textarea">${post.description}</textarea>
      <br>
      <input class="basic-button" type="file" id="new_post_photo" name="new_post_photo">
      <br>
      <button type="submit" id="save_edited_post_button" class="basic-button">Save</button>
  </form>
  `);
  });
}