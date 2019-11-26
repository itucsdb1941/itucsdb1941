import { Component, OnInit } from '@angular/core';
import { Food } from '../../models/app.model';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'recipe',
  templateUrl: './recipe.component.html',
  styleUrls: ['./recipe.component.css']
})


export class RecipeComponent implements OnInit {

  	recipes: any[];
	foods: any[] = [];
	Id : any;
	type: string ;
	
	constructor(private route: ActivatedRoute, private appService: AppService, private router: Router) { 
		this.Id = this.route.snapshot.paramMap.get("id");
		this.type = this.route.snapshot.url[1].path;
		console.log(this.Id)
		
	}
	
	ngOnInit() {
		this.recipe();
	}

	recipe(): void {
		this.appService.recipePage(this.Id, this.type).subscribe(recipe => this.recipes = recipe);
	
	}
}
