import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'drink-menu',
  templateUrl: './drink-menu.component.html',
  styleUrls: ['./drink-menu.component.css']
})
export class DrinkMenuComponent implements OnInit {

  	drinks: any[] = [];

	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 

	}
	
	
	ngOnInit() {
		this.getDrinks();
	}
	
	getDrinks(): void {
		this.appService.drinkMenu().subscribe(drink => this.drinks = drink);
		console.log(this.drinks);
	}
	home(): void{	
		this.router.navigateByUrl('/foods-list');		
	}
}
