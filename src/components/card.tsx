import './card.css'

interface CardProps {
    username: String;
    starts: number;
    type: String;
    attack: Number;
    defense: Number;
}

export default function Card(props: CardProps) {
    var starArray = []
    
    for (var i = 0; i < Math.min(props.starts, 12); i++) {
        starArray.push(<img className='star' src="src/assets/cards/star.png"></img>)
    }

    return (
        <div id='cardContainer'>
            <img id='cardTemplate' src="src/assets/cards/it1.png"></img>
            <div id='nameContainer'>
                <h1 id='cardName'>{props.username}</h1>
                <img src="src/assets/cards/c++.svg.png" id='attribute'></img>
            </div>
            <div id='starsContainer'>
                {starArray}
            </div>
            <div id='imageContainer'>
                <img src='src/assets/cards/itadrias.png' id='cardImg'></img>
            </div>
            <div id='textContainer'>
                <label id='cardType'> [{props.type}/Spellcaster] </label>
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