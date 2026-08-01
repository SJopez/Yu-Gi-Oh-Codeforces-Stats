const images = import.meta.glob('/src/assets/*.{png,jpg}', { eager: true, import: 'default' });
import Card from './card';
import './disk.css'

interface DiskOptions {
    width: number
}

export default function DuelDisk(props: DiskOptions){
    
    return (
        <div id="diskContainer">
            <img id='diskImage' src={`${images["/src/assets/character.png"]}`}></img>
            <Card 
                username={"Yo"} 
                starts={8} 
                type={"Pollazo"} 
                attack={4000} 
                defense={1200} 
                rank={"expert"} 
                photo={""} 
                glow={true} 
                sparkle={true} 
                effectOpacity={0.7}
                nameEffect={true}
                width={props.width}
                preffix='mini1'
                scale={true}>     
            </Card>
            <Card 
                username={"Yo"} 
                starts={8} 
                type={"Pollazo"} 
                attack={4000} 
                defense={1200} 
                rank={"expert"} 
                photo={""} 
                glow={true} 
                sparkle={true} 
                effectOpacity={0.7}
                nameEffect={true}
                width={props.width}
                preffix='mini2'
                scale={true}>     
            </Card>
            <Card 
                username={"Yo"} 
                starts={8} 
                type={"Pollazo"} 
                attack={4000} 
                defense={1200} 
                rank={"expert"} 
                photo={""} 
                glow={true} 
                sparkle={true} 
                effectOpacity={0.7}
                nameEffect={true}
                width={props.width}
                preffix='mini3'
                scale={true}>     
            </Card>
            <Card 
                username={"Yo"} 
                starts={8} 
                type={"Pollazo"} 
                attack={4000} 
                defense={1200} 
                rank={"expert"} 
                photo={""} 
                glow={true} 
                sparkle={true} 
                effectOpacity={0.7}
                nameEffect={true}
                width={props.width}
                preffix='mini4'
                scale={true}>     
            </Card>
            <Card 
                username={"Yo"} 
                starts={8} 
                type={"Pollazo"} 
                attack={4000} 
                defense={1200} 
                rank={"expert"} 
                photo={""} 
                glow={true} 
                sparkle={true} 
                effectOpacity={0.7}
                nameEffect={true}
                width={props.width}
                preffix='mini5'
                scale={true}>     
            </Card>                     
        </div>
    )
}