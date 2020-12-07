var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var width = canvas.width;
var height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
ctx.lineWidth = 7;
var vasePreset = 1;
var vaseFragment = 1;
var numVases = 10;
var numFrags = 1125;
var fill_value = false;
var stroke_value = true;
var canvas_data = {"pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": []}

ctx.fillStyle = "#FFFFFF";
ctx.fillRect(0, 0, 512, 512);

function color(color_value){
    ctx.strokeStyle = color_value;
    ctx.fillStyle = color_value;
}    

function update_lw() {
    document.getElementById("line_width_val").innerText = 'Brush Size ' + String(ctx.lineWidth);
}

function add_pixel(){
    ctx.lineWidth += 1;
    update_lw();
}
        
function reduce_pixel(){
    if (ctx.lineWidth == 1){
        ctx.lineWidth = 1;
    }
    else{
        ctx.lineWidth -= 1;
    }
    update_lw();
}
        
function fill(){
    fill_value = true;
    stroke_value = false;
}
        
function outline(){
    fill_value = false;
    stroke_value = true;
}
               
function reset(){
    ctx.fillStyle = "#ffffff";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillRect(0, 0, 512, 512);
    canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] }
}

function update_vase() {
    document.getElementById("vase_preset_val").innerText = 'Vase Outline ' + String(vasePreset);
    var preset = new Image();
    preset.src = 'preset/' + String(vasePreset);
    preset.onload = function(){
        ctx.drawImage(preset, 0, 0);
    };
}

function next_vase() {
    vasePreset = (vasePreset % numVases) + 1;
    update_vase();
}

function prev_vase() {
    vasePreset = (vasePreset - 2 + numVases) % numVases + 1;
    update_vase();
}

function update_frag() {
    document.getElementById("vase_fragment").innerText = 'Vase Fragment ' + String(vaseFragment);
    var frag = new Image();
    frag.src = 'chopped/' + String(vaseFragment);
    frag.onload = function(){
        var pattern = ctx.createPattern(this, "repeat");
        ctx.fillStyle = pattern;
        ctx.fill();
    };
}

function random_fragment() {
    vaseFragment = Math.floor((Math.random() * numFrags));
    update_frag();
}

function next_frag() {
    vaseFragment = (vaseFragment % numFrags) + 1;
    update_frag();
}

function prev_frag() {
    vaseFragment = (vaseFragment - 2 + numFrags) % numFrags + 1;
    update_frag();
}
        
// pencil tool
        
function pencil(){
        
    canvas.onmousedown = function(e){
        hold = true;
        ctx.beginPath();
        //ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function(e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw(e);
        }
    };
        
    canvas.onmouseup = function(e){
        hold = false;
    };
        
    canvas.onmouseout = function(e){
        hold = false;
    };
        
    function draw(e){
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}
        
// line tool
        
function line(){
           
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.offsetX;
        prevY = e.offsetY;
        hold = true;
    };
            
    canvas.onmousemove = function linemove(e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.offsetX;
            curY = e.offsetY;
            ctx.beginPath();
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            canvas_data.line.push({ "starx": prevX, "starty": prevY, "endx": curX, "endY": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
            ctx.closePath();
        }
    };
            
    canvas.onmouseup = function (e){
         hold = false;
    };
            
    canvas.onmouseout = function (e){
         hold = false;
    };
}
        
// rectangle tool
        
function rectangle(){
            
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.offsetX;
        prevY = e.offsetY;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.offsetX - prevX;
            curY = e.offsetY - prevY;
            ctx.strokeRect(prevX, prevY, curX, curY);
            if (fill_value){
                ctx.fillRect(prevX, prevY, curX, curY);
            }
            canvas_data.rectangle.push({ "starx": prevX, "stary": prevY, "width": curX, "height": curY, "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value, "fill_color": ctx.fillStyle });
            
        }
    };
            
    canvas.onmouseup = function(e){
        hold = false;
    };
            
    canvas.onmouseout = function(e){
        hold = false;
    };
}
        
// circle tool
        
function circle(){
            
    canvas.onmousedown = function (e){
        img = ctx.getImageData(0, 0, width, height);
        prevX = e.offsetX;
        prevY = e.offsetY;
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            curX = e.offsetX;
            curY = e.offsetY;
            ctx.beginPath();
            ctx.arc(Math.abs(curX + prevX)/2, Math.abs(curY + prevY)/2, Math.sqrt(Math.pow(curX - prevX, 2) + Math.pow(curY - prevY, 2))/2, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.stroke();
            if (fill_value){
               ctx.fill();
            }
            canvas_data.circle.push({ "starx": prevX, "stary": prevY, "radius": curX - prevX, "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value, "fill_color": ctx.fillStyle });
        }
    };
            
    canvas.onmouseup = function (e){
        hold = false;
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}
        
// eraser tool
        
function eraser(){
    
    canvas.onmousedown = function(e){
        curX = e.offsetX;
        curY = e.offsetY;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function(e){
        if(hold){
            curX = e.offsetX;
            curY = e.offsetY;
            draw();
        }
    };
        
    canvas.onmouseup = function(e){
        hold = false;
    };
        
    canvas.onmouseout = function(e){
        hold = false;
    };
        
    function draw(){
        ctx.lineTo(curX, curY);
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }    
}  

function save(){
    var filename = document.getElementById("fname").value;
    var data = JSON.stringify(canvas_data);
    var image = canvas.toDataURL();
    
    $.post("/", { save_fname: filename, save_cdata: data, save_image: image });
    alert(filename + " saved");
}

function convert_success(resp) {
    document.getElementById("vase").src = 'data:image/jpg;base64,' + resp;
//    console.log('resp');
//    console.log(resp);
}

function convert() {
    var image = canvas.toDataURL('image/png');

    resp = $.ajax({
        type: "POST",
        url: "/",
        data: { drawn_image: image },
        success: convert_success,
//        dataType: "json",
    });

}
