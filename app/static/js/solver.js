function updateColor(object) {
    const pin = object.getAttribute("data-pin");
    const color = object.getAttribute("data-color");
    document.getElementById("inputPin"+pin).style.backgroundColor=color;
    document.getElementById("inputPin"+pin).setAttribute("data-pin",color)
}

function end() {
    var replace = document.createElement("a");
    replace.innerHTML = "Enter New Code";
    replace.classList.add("btn");
    replace.classList.add("btn-light");
    replace.classList.add("w-auto");
    replace.classList.add("text-secondary");
    replace.href = "/solver";
    document.getElementById("sender").replaceWith(replace);
}

function code() {
    $.ajax({
        type:'POST',
        url:'/solver',
        data:{
            pin1:document.getElementById("inputPin1").getAttribute("data-pin"),
            pin2:document.getElementById("inputPin2").getAttribute("data-pin"),
            pin3:document.getElementById("inputPin3").getAttribute("data-pin"),
            pin4:document.getElementById("inputPin4").getAttribute("data-pin")
        }
    })
    .done(function(data){
        end();
        if (!data.done) {
            var message = document.createElement("p");
            message.innerHTML = "The Bot failed to find the code...";
            message.classList.add("text-primary");
            message.classList.add("h4");
            message.classList.add("text-center");
            document.getElementById("message").replaceWith(message);
        }
        else {
            document.getElementById("tries").innerHTML=data.tries;
            document.getElementById("message").style.display="inline";
        }
        for (let r = 1; r <= data.tries; r++) {
            var box=document.getElementById("row"+r);
            box.style.display="flex";
            document.getElementById("row"+r+"pin1").style.backgroundColor=data.moves[r-1][0];
            document.getElementById("row"+r+"pin2").style.backgroundColor=data.moves[r-1][1];
            document.getElementById("row"+r+"pin3").style.backgroundColor=data.moves[r-1][2];
            document.getElementById("row"+r+"pin4").style.backgroundColor=data.moves[r-1][3];
            for (let i = 1; i <= data.w[r-1]; i++) {
                document.getElementById("row"+r+"white"+i.toString()).style.backgroundColor="white";
            }
            for (let i = 1; i <= data.r[r-1]; i++) {
                document.getElementById("row"+r+"red"+i.toString()).style.backgroundColor="black";
            }
        }
    });
}