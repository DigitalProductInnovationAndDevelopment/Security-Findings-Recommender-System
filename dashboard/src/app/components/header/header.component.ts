import { Component, OnInit } from '@angular/core';
import { ThemeService } from 'src/app/services/theme.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor(private themeService: ThemeService) {}
  ngOnInit(): void {
this.setTheme('light')
  }

  setTheme(mode: 'dark'|'light') {
    this.themeService.setTheme(mode);
    localStorage.setItem('theme', JSON.stringify(mode))
  }

}
