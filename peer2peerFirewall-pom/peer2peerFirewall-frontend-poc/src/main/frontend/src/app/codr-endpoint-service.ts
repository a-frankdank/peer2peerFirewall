import { Injectable } from '@angular/core';

import { CodrEndpoint } from './codr-endpoint';
import { CODRENDPOINTS } from './mock-codr-endpoints';

@Injectable()
export class CodrEndpointService{
    getCodrEndpoints(): CodrEndpoint[]{
        return CODRENDPOINTS;
    } 
}