//A class Repersenting each new pattern
class Pattern{
    constructor(conainter, id){
        this.container = conainter;
        this.id=id;

        this.button = this.createSelf();
    }
    createSelf(){
        const btn = document.createElement('button');
        btn.textContent = "Choose Pattern";
        btn.classList.add("patternButton");

        const hiddenUpload = document.createElement('input')
        hiddenUpload.type = 'file'
        hiddenUpload.accept = 'image/*'
    
       
        
        btn.addEventListener("click", () => {
            hiddenUpload.click();
        });

        hiddenUpload.addEventListener("change", (event) =>{
            const file = event.target.files[0];
            if (file){
                if(file.type == 'image/jpeg' || file.type == 'image/png'){
                    this.addImg(file);
                }else{
                    alert("Please select jpeg, or png file");
                }
                
            }else{
                console.log('File Not selected');
            }
        })

        this.container.appendChild(btn);
        return btn;
    }
    
    
    addImg(file){
        const img = document.createElement("img");
        const imgUrl = URL.createObjectURL(file);
        img.src = imgUrl;     // path to your image
        
        img.onload = function() {
            URL.revokeObjectURL(imgUrl); 
        };
        
        img.alt = "Quilt Pattern";         // accessibility
        this.button.textContent = '';

        this.button.appendChild(img);
    }
}


//repersents the button that adds new patterns
class plusPattern{
    constructor(conainterId){
       
        this.container = document.getElementById(conainterId);
        this.count = 0;
        this.button = this.createSelf();
        this.patterns = [];
    }

    createSelf(){

        const btn = document.createElement('button');
        btn.textContent = "New Pattern";
        btn.classList.add("plusButton")

        btn.addEventListener("click", () => {
          this.patterns.push(new Pattern(this.container, this.count++));
        });
        
        this.container.appendChild(btn);
        return btn;
    }    
}


class Quilt{
    constructor(containerId){
        container = document.getElementById(containerId)
    }
}


class Tile{
    constructor(container){
        this.container = container;
    }
}




const buttonSpawner = new plusPattern('button-container');
const quiltSpawner = new Quilt('quilt-layout');
