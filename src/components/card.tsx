import './card.css'
const images = import.meta.glob('/src/assets/cards/*.{png,jpg}', { eager: true, import: 'default' });
const effects = import.meta.glob('/src/assets/cards/effects/*.png', { eager: true, import: 'default' });

interface CardProps {
    username: String;
    rank: String;
    starts: number;
    type: String;
    attack: Number;
    defense: Number;
}


function Attribute(){
    return (
        <div id='langContainer'>
            <img id="attribute" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-plain.svg" />
        </div>
    )
}
export function Sparkle() {
  return (
    <div className="sparkle">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
}
export function CardGlow() {
  return (
    <svg className="card-glow" viewBox="0 0 408 612">
      <rect
        className="card-glow-path"
        x="23"
        y="42"
        width="360"
        height="520"
        rx="13"
      />
    </svg>
  );
}
export default function Card(props: CardProps) {
    var starArray = []
    
    for (var i = 0; i < Math.min(props.starts, 12); i++) {
        starArray.push(<img className='star' src={images['/src/assets/cards/star.png'] as string}></img>)
    }

    return (
        <div id='cardContainer'>
            <CardGlow></CardGlow>
            <Sparkle></Sparkle>
            <img id='effect' src={effects[`/src/assets/cards/effects/${props.rank}.png`] as string}></img>
            <img id='cardTemplate' src={images[`/src/assets/cards/${props.rank}.png`] as string}></img>
            <div id='nameContainer'>
                <h1 id='cardName'>{props.username}</h1>
                <Attribute></Attribute>
            </div>
            <div id='starsContainer'>
                {starArray}
            </div>
            <div id='imageContainer' style = {{ backgroundImage: `url(${images[`/src/assets/cards/tourist.jpg`]})` }}>
                
            </div>
            <div id='textContainer'>
                <label id='cardType'> [{props.type}] </label>
                <div id='descriptionContainer' className='scrollable'>
                    <p id='description'>
                        Requires 3 Tributes to Normal Summon (cannot be Normal Set). This card's Normal Summon cannot be negated.  
                    </p>
                </div>
                <hr id='separator'></hr>
                <div id='statsContainer'>
                    <label id='atk'>ATK/{props.attack.toString()}</label>
                    <label id='def'>DEF/{props.defense.toString()}</label>
                </div>
            </div>
        </div>
    )
}