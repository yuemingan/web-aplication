var entering = true;
let stack = [];
stack.push(0);

function digitClick(buttonElement) {
    if (entering) {
        let bottom = stack[stack.length - 1];
        bottom = bottom * 10 + parseInt(buttonElement.innerHTML);
        stack[stack.length - 1] = bottom;
        document.getElementById("output").innerHTML = bottom;
        document.getElementById("output").style.backgroundColor = "moccasin";
    } else {
        if (stack.length >= 3) {
            document.getElementById("output").innerHTML = "stack overflow";
            document.getElementById("output").style.backgroundColor = "red";
            stack = [];
            stack.push(0);
            entering = true;
        } else {
            stack.push(0);
            entering = true;
            let bottom = stack[stack.length - 1];
            bottom = bottom * 10 + parseInt(buttonElement.innerHTML);
            stack[stack.length - 1] = bottom;
            document.getElementById("output").innerHTML = bottom;
            document.getElementById("output").style.backgroundColor = "moccasin";
        }

    }



}

function pushClick() {
    if (stack.length == 3) {
        document.getElementById("output").innerHTML = "stack overflow";
        document.getElementById("output").style.backgroundColor = "red";
        stack = [];
        stack.push(0);
        entering = true;
    } else {
        stack.push(0);
        document.getElementById("output").innerHTML = 0;
        entering = true;
        document.getElementById("output").style.backgroundColor = "moccasin";
    }
}

function opClick(buttonElement) {
    if (stack.length < 2) {
        document.getElementById("output").innerHTML = "stack underflow";
        document.getElementById("output").style.backgroundColor = "red";
        stack = [];
        stack.push(0);
        entering = true;
    } else {
        let second = stack.pop();
        let first = stack.pop();
        if (second == 0) {
            document.getElementById("output").innerHTML = "divide by zero";
            document.getElementById("output").style.backgroundColor = "red";
        stack = [];
        stack.push(0);
        entering = true;
        } else {
            let operation = buttonElement.id.substr(4);
            let result;
            switch (operation) {
                case 'plus':
                    result = first + second;
                    break;
                case 'minus':
                    result = first - second;
                    break;
                case 'times':
                    result = first * second;
                    break;
                case 'divide':
                    result = parseInt(first / second);
                    break;
                default:
                    break;
            }
            stack.push(result);
            document.getElementById("output").innerHTML = result;
            document.getElementById("output").style.backgroundColor = "green";
            entering = false;
        }
    }
}

