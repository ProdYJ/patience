let myBtnON = document.querySelector('input.ON_btn');
let myDiode1 = document.querySelector('img.d1');
let myBtnM = document.querySelector('input.Manual_btn');
let myDiode2 = document.querySelector('img.d2');
let myBtnOFF = document.querySelector('input.OFF_btn');
let myDiode3 = document.querySelector('img.d3');
let manualOpen = document.querySelector('input.actionOpen');
let manualClose = document.querySelector('input.actionClose');
let mode;

if (!localStorage.getItem('x')) {
  alert('Aucune valeur d état trouvée');
} 
else {
  let storedMode = localStorage.getItem('x');
  if (storedMode==0) {
    actionBtnOFF ();
  }
  else if (storedMode==1) {
    actionBtnON ();
  }
  else {
    actionBtnM ();
  }
}

myBtnON.addEventListener('click', function() {
  mode = 1;
  localStorage.setItem('x', mode);
	resetBtn ();
  actionBtnON ();
});

myBtnM.addEventListener('click', function() {
  mode = 2;
  localStorage.setItem('x', mode);
	resetBtn ();
  actionBtnM ();
});

myBtnOFF.addEventListener('click', function() {
  mode = 0;
  localStorage.setItem('x', mode);
	resetBtn ();
  actionBtnOFF ();
});

manualOpen.addEventListener('click', function() {
	checkManual ();
});

manualClose.addEventListener('click', function() {
	checkManual ();
});




function resetBtn() {
	myDiode1.setAttribute('src', '../static/img/diodeOFF.png');
	myDiode2.setAttribute('src', '../static/img/diodeOFF.png');
	myDiode3.setAttribute('src', '../static/img/diodeOFF.png');
}

function actionBtnON() {
	let mySrc = myDiode1.getAttribute('src');
    if (mySrc === '../static/img/diodeOFF.png') {
      myDiode1.setAttribute('src', '../static/img/diodeON.png');
    } else {
      myDiode1.setAttribute('src', '../static/img/diodeOFF.png');
    }
}

function actionBtnM() {
	let mySrc = myDiode2.getAttribute('src');
    if (mySrc === '../static/img/diodeOFF.png') {
      myDiode2.setAttribute('src', '../static/img/diodeON.png');
    } else {
      myDiode2.setAttribute('src', '../static/img/diodeOFF.png');
    }
}

function actionBtnOFF() {
	let mySrc = myDiode3.getAttribute('src');
    if (mySrc === '../static/img/diodeOFF.png') {
      myDiode3.setAttribute('src', '../static/img/diodeON.png');
    } else {
      myDiode3.setAttribute('src', '../static/img/diodeOFF.png');
    }
}

function checkManual() {
	let mySrc = myDiode2.getAttribute('src');
	if (mySrc === '../static/img/diodeOFF.png') {
		alert('ATTENTION, Mode Manuel désactivé');
	}
}