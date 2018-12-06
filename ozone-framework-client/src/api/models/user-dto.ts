import { Model, Property } from "../../lib/openapi/decorators";

import { IdDto } from "./id-dto";

import { createLazyComponentValidator } from "../common";


@Model({ name: "User" })
export class UserDTO {

    static validate = createLazyComponentValidator(UserDTO);

    @Property()
    id: number;

    @Property()
    username: string;

    @Property()
    userRealName: string;

    @Property()
    email: string;

    @Property({ nullable: true })
    hasPWD?: string;

    @Property({ nullable: true, readOnly: true })
    lastLogin?: string;

    @Property({ readOnly: true })
    totalDashboards: number;

    @Property({ readOnly: true })
    totalGroups: number;

    @Property({ readOnly: true })
    totalStacks: number;

    @Property({ readOnly: true })
    totalWidgets: number;

}


@Model()
export class UserGetResponse {

    static validate = createLazyComponentValidator(UserGetResponse);

    @Property()
    success: boolean;

    @Property()
    results: number;

    @Property(() => UserDTO)
    data: UserDTO[];

}


export interface UserCreateRequest {
    username: string;
    userRealName: string;
    email: string;
}


@Model()
export class UserCreateResponse {

    static validate = createLazyComponentValidator(UserCreateResponse);

    @Property()
    success: boolean;

    @Property(() => UserDTO)
    data: UserDTO[];
}


export interface UserUpdateRequest {
    id: number;
    username: string;
    userRealName: string;
    email: string;
}


@Model()
export class UserUpdateResponse {

    static validate = createLazyComponentValidator(UserUpdateResponse);

    @Property()
    success: boolean;

    @Property(() => UserDTO)
    data: UserDTO[];

}


@Model()
export class UserDeleteResponse {

    static validate = createLazyComponentValidator(UserDeleteResponse);

    @Property()
    success: boolean;

    @Property(() => IdDto)
    data: IdDto[];

}

