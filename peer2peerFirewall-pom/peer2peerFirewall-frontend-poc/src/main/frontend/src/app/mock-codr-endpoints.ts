import { CodrEndpoint } from './codr-endpoint';

export const CODRENDPOINTS: CodrEndpoint[] = [
    {
        dstAdress: "0.0.0.0",
        dstPort: "12",
        label: "",
        srcAdress: "0.0.0.1",
        srcPort: "34",
        timeLastChanged: new Date(Date.now())
    },
    {
        dstAdress: "127.0.0.1",
        dstPort: "56",
        label: "",
        srcAdress: "127.0.0.2",
        srcPort: "78",
        timeLastChanged: new Date(Date.now())
    }
    ,
    {
        dstAdress: "172.0.0.2",
        dstPort: "910",
        label: "",
        srcAdress: "172.0.0.3",
        srcPort: "1112",
        timeLastChanged: new Date(Date.now())
    }
];
