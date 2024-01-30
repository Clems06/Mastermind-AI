function updateColor(object) {
    const pin = object.getAttribute("data-pin");
    const color = object.getAttribute("data-color");
    document.getElementById("printPin"+pin).style.backgroundColor=color;
    document.getElementById("printPin"+pin).setAttribute("data-pin",color)
}

function end(pin1, pin2, pin3, pin4, m) {
    var message = document.createElement("p");
    message.innerHTML = m;
    message.classList.add("text-primary");
    message.classList.add("h4");
    message.classList.add("text-center");
    document.getElementById("message").replaceWith(message);
    if (pin1!="") {
        document.getElementById("pin1").style.backgroundColor=pin1;
        document.getElementById("pin2").style.backgroundColor=pin2;
        document.getElementById("pin3").style.backgroundColor=pin3;
        document.getElementById("pin4").style.backgroundColor=pin4;
    }
    for (let i = 1; i < 5; i++) {
        document.getElementById("pin"+i).classList.add("border-primary");
        document.getElementById("pin"+i).classList.remove("border-light");
    }
    document.getElementById("pin4").classList.add("border-primary");
    document.getElementById("pin4").classList.remove("border-light");
    var replace = document.createElement("a");
    replace.innerHTML = "Start New Game";
    replace.classList.add("btn");
    replace.classList.add("btn-light");
    replace.classList.add("w-auto");
    replace.classList.add("text-secondary");
    replace.href = "/game";
    document.getElementById("sender").replaceWith(replace);
}

function answer(optional_text="") {
    $.ajax({
        type:'POST',
        url:'/game',
        data:{
            answer:"true"
        }
    })
    .done(function(data){
        end(data.a_pin1, data.a_pin2, data.a_pin3, data.a_pin4, optional_text+"This was the correct password");
    })
}

function sub() {
    $.ajax({
        type:'POST',
        url:'/game',
        data:{
            pin1:document.getElementById("printPin1").getAttribute("data-pin"),
            pin2:document.getElementById("printPin2").getAttribute("data-pin"),
            pin3:document.getElementById("printPin3").getAttribute("data-pin"),
            pin4:document.getElementById("printPin4").getAttribute("data-pin")
        }
    })
    .done(function(data){
        if (data.correct==true) {
            end("", "", "", "", "Bravo ! You won in "+data.tries+" tries");
        } else if (data.tries==12) {
            answer("You spent all your tries...");
        }
        document.getElementById("tries").innerHTML=12-data.tries;
        box=document.getElementById("row"+data.tries);
        box.style.display="flex";
        document.getElementById("row"+data.tries+"pin1").style.backgroundColor=data.old_pin1;
        document.getElementById("row"+data.tries+"pin2").style.backgroundColor=data.old_pin2;
        document.getElementById("row"+data.tries+"pin3").style.backgroundColor=data.old_pin3;
        document.getElementById("row"+data.tries+"pin4").style.backgroundColor=data.old_pin4;
        for (let i = 1; i < data.w+1; i++) {
            document.getElementById("row"+data.tries+"white"+i.toString()).style.backgroundColor="white";
        }
        for (let i = 1; i < data.r+1; i++) {
            document.getElementById("row"+data.tries+"red"+i.toString()).style.backgroundColor="black";
        }
    });
}