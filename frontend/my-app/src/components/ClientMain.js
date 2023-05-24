import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom";
import jwt_decode from "jwt-decode";
import useToken from './useToken';
import NavMenu from './NavMenu';

class ImageGrid extends React.Component {

    constructor(props) {
        super(props);
        this.state = { 
            images: [
                {name:'Image 1',src:'//placeimg.com/600/400?text=1',desc:'This describes this image..'},
                {name:'Image 2',src:'//placeimg.com/600/400?text=2',desc:'This describes this image 2..'},
                {name:'Image 3',src:'//placeimg.com/600/400/any',desc:'This describes this image 3 ..'},
                {name:'Image 4',src:'//placeimg.com/600/400?text=4',desc:'This describes this image 4..'},
                {name:'Image 5',src:'//placeimg.com/600/400?text=5',desc:'This describes this image 5..'},
                {name:'Image 6',src:'//placeimg.com/600/400?text=6',desc:'This describes this image 6..'},
                // "id": int, "location": { "id": int, "country": string, "county": string, "settlement": string, "street": string, "number": itn }, "title": string, "description": string, "arrivalDate": string, "leaveDate": string, "image": string, "isPublic": boolean, "userID": int } 
            ],
            currentSelection: {},
        };
        this.handleClick = this.handleClick.bind(this);
    }
    
    componentDidMount() {
        // set first image selected
        this.setState({ currentSelection: this.state.images[0] });
    }
    
    handleClick(val) {
        //console.log(val)
        this.setState({ currentSelection: val });
    }
    
    render(){
        var { images, currentSelection } = this.state;
        return(
        <div>
            <div className="row">
                <div className="col-md">
                    <div className="row no-gutters">
                    {images.map((val, k) => {
                        return (
                        <div className="col-sm-4" key={k}>
                            <img src={val.src} className={'img-fluid ' + (val.src===currentSelection.src?'p-1':'')} onClick={() => this.handleClick(val)} />
                        </div>)
                        })
                    }
                     </div>
                </div>
                <div className="col-md">
                    <h3 className="font-weight-light">{ currentSelection.name }</h3>
                    <p>{ currentSelection.desc }</p>
                </div>
            </div>
        </div>
        )
    }
};

export default function (props) {

    const { token, setToken } = useToken();

    const [decoded, setDecoded] = useState({});

    useEffect(() => {
        if(token)
        setDecoded(jwt_decode(token));
      }, []);

    return (
        <div>
      <NavMenu/>
        <div className="container-fluid py-3">
            
            <h4 className="text-center font-weight-light text-light mb-3">{decoded.role}</h4>
            <ImageGrid />
        </div>
        </div>
    )
  }