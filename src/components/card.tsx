import './card.css'

interface CardProps {
    username: String;
    starts: number;

}

export default function Card(props: CardProps) {
    var starArray = []
    
    for (var i = 0; i < Math.min(props.starts, 12); i++) {
        starArray.push(<img className='star' src="src/assets/cards/star.png"></img>)
    }

    return (
        <div id='cardContainer'>
            <img id='cardTemplate' src="src/assets/cards/expert1.png"></img>
            <div id='nameContainer'>
                <h1 id='cardName'>{props.username}</h1>
            </div>
            <div id='starsContainer'>
                {starArray}
            </div>
            <div id='imageContainer'>
                <img src='src/assets/cards/itadrias.png' id='cardImg'></img>
            </div>
        </div>
    )
}