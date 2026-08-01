const images = import.meta.glob('/src/assets/*.{png,jpg}', { eager: true, import: 'default' });
import Card from './card';
import './disk.css'

interface DiskOptions {
    width: number
}

export default function DuelDisk(props: DiskOptions){
    var usernameList = ["sergio22", "sn0wm4n", "itadrias", "EduardoBrito", "jiangly"]
    var cardList = []

    for (var i = 0; i < 5; i++){
        var user = usernameList[i]
        cardList.push(
            <Card 
                username={user}
                stars={1}
                preffix={`mini${i + 1}`}
                width={props.width}
                scale={true}>     
            </Card>
        )
    }

    return (
        <div id="diskContainer">
            <img id='diskImage' src={`${images["/src/assets/character.png"]}`}></img>
            {cardList}                     
        </div>
    )
}