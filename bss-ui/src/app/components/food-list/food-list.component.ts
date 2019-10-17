import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'food-list',
  templateUrl: './food-list.component.html',
  styleUrls: ['./food-list.component.css']
})
export class FoodListComponent implements OnInit {

  foods: Food[] = [];

	constructor(private route: ActivatedRoute, private appService: AppService) { }

	ngOnInit() {
		this.getFoods();
		//console.log(this.foods);
	}

	getFoods(): void {
		this.appService.getFood().subscribe(food => this.foods = food);
	}
  

}
