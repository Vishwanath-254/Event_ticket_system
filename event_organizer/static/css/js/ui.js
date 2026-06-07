const cards=document.querySelectorAll(".event-card")

cards.forEach(card=>{
card.addEventListener("mouseover",()=>{
card.style.transform="scale(1.02)"
})

card.addEventListener("mouseout",()=>{
card.style.transform="scale(1)"
})
})