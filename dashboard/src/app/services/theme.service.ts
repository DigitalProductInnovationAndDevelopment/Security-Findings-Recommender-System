import { Injectable } from "@angular/core";
import cssVars from "css-vars-ponyfill";
import { darkTheme, lightTheme } from "src/Themes";
import { ITheme } from "../interfaces/ITheme";

@Injectable({
    providedIn: 'root'
})
export class ThemeService {
    public setTheme(mode: 'light' | 'dark'): void {
        const variables = this.getThemeVariables(mode);
        this.setColorVariables(variables);
        document.documentElement.setAttribute('data-mode', mode);
    }

    private getThemeVariables(mode: 'light' | 'dark'): ITheme {
        return mode === 'dark' ? darkTheme : lightTheme;
    }

    private setColorVariables(colorPalette: ITheme): void {
        cssVars({
            variables: {
                ...colorPalette
            }
        })
    }
}