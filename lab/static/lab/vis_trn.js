const visDivs = document.getElementsByClassName("vis-div");
const vis1 = document.getElementById("vis-1");
const vis2 = document.getElementById("vis-2");
const vis3 = document.getElementById("vis-3");
const vis4 = document.getElementById("vis-4");
const canvas = document.getElementById("align-canvas");

let count = 0;
let created = false;

let mouse = {
    x: 0,
    y: 0, 
    startX: 0,
    startY: 0
};

let startTop = 0;
let startLeft = 0;

let vis1Moving = false;
let vis2Moving = false;
let vis3Moving = false;
let vis4Moving = false;

/* -----------------------------------------------------------*/


function setMousePosition(e) {
    mouse.x = e.clientX-canvas.offsetLeft;
    mouse.y = e.clientY-canvas.offsetTop;   
};
function setMouseStart(){
    mouse.startX = mouse.x;
    mouse.startY = mouse.y;
}

function setDivStart(my_div) {
    startTop = parseInt(my_div.style.top,10)
    startLeft = parseInt(my_div.style.left,10)
}


function setDivs(canvas){

    canvas.onmousemove = function (e) {
        setMousePosition(e);

        if (vis1Moving){
            vis1.style.top = startTop + (mouse.y - mouse.startY) +'px';
            vis1.style.left = startLeft + (mouse.x - mouse.startX) +'px';
            /* console.log(parseInt(vis1.style.left,10), parseInt(vis1.style.top,10)) */
        }
        if (vis2Moving){
            vis2.style.top = startTop + (mouse.y - mouse.startY) +'px';
            vis2.style.left = startLeft + (mouse.x - mouse.startX) +'px';
        }
        if (vis3Moving){
            vis3.style.top = startTop + (mouse.y - mouse.startY) +'px';
            vis3.style.left = startLeft + (mouse.x - mouse.startX) +'px';
        }
        if (vis4Moving){
            vis4.style.top = startTop + (mouse.y - mouse.startY) +'px';
            vis4.style.left = startLeft + (mouse.x - mouse.startX) +'px';
        }
    }    

    canvas.onclick = function (e) {

        if (!created){

                if (count == 0) {

                    canvas.appendChild(vis1)
                    vis1.style.display = 'inline-block'
                    vis1.style.position = 'relative'
                    vis1.style.left = mouse.x + 'px';
                    vis1.style.top = mouse.y - 15 + 'px';
                    vis1.style.margin = '-1.5px';
        
                }
                if (count == 1) {
        
                    canvas.appendChild(vis2)
                    vis2.style.display = 'inline-block'
                    vis2.style.position = 'relative'
                    vis2.style.left = mouse.x + 'px';
                    vis2.style.top = mouse.y -15 + 'px';
                    vis2.style.margin = '-1.5px';
                }
                if (count == 2) {
        
                    canvas.appendChild(vis3)
                    vis3.style.display = 'inline-block'
                    vis3.style.position = 'relative'
                    vis3.style.left = mouse.x + 'px';
                    vis3.style.top = mouse.y -15 + 'px';
                    vis3.style.margin = '-1.5px';
        
                }
                if (count == 3) {
        
                    canvas.appendChild(vis4)
                    vis4.style.display = 'inline-block'
                    vis4.style.position = 'relative'
                    vis4.style.left = mouse.x + 'px';
                    vis4.style.top = mouse.y -15 + 'px';
                    vis4.style.margin = '-1.5px';
        
                }
                count++;
                if (count == 4) {
                    created = true;
                }
        }

        if (created) {
            let myVis1 = [
                parseInt(vis1.style.left,10),
                parseInt(vis1.style.top,10)
            ]
            let myTest3 = [myVis1,myVis1]
            console.log(myVis1, myVis1.toString(), myTest3, myTest3.toString())
        }
    }

    document.onmouseup = function (e) {
        vis1Moving = false;
        vis2Moving = false;
        vis3Moving = false;
        vis4Moving = false;
    }

    vis1.onmousedown = function (e) {
        console.log('vis1 clicked')
        vis1Moving = true;
        setMouseStart();
        setDivStart(vis1);
    }
    vis2.onmousedown = function (e) {
        vis2Moving = true;
        setMouseStart();
        setDivStart(vis2);
    }
    vis3.onmousedown = function (e) {
        vis3Moving = true;
        setMouseStart();
        setDivStart(vis3);
    }
    vis4.onmousedown = function (e) {
        vis4Moving = true;
        setMouseStart();
        setDivStart(vis4);
        console.log('hello')
    }


}


function saveCoordsSubmit() {
    let myVis1 = [
        parseInt(vis1.style.left,10)/canvas.offsetWidth,
        parseInt(vis1.style.top,10)/canvas.offsetHeight
    ]
    let myVis2 = [
        parseInt(vis2.style.left,10)/canvas.offsetWidth,
        parseInt(vis2.style.top,10)/canvas.offsetHeight
    ]
    let myVis3 = [
        parseInt(vis3.style.left,10)/canvas.offsetWidth,
        parseInt(vis3.style.top,10)/canvas.offsetHeight
    ]
    let myVis4 = [
        parseInt(vis4.style.left,10)/canvas.offsetWidth,
        parseInt(vis4.style.top,10)/canvas.offsetHeight
    ]
    let myNum = '[['+myVis1+'],['+myVis2+'],['+myVis3+'],['+myVis4+']]'
    document.getElementById('vis-coords').value = myNum
}